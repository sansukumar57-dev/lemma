"""Re-prefix app (ex-desk) asset storage: ``desks/<id>/...`` -> ``apps/<id>/...``.

Background: the desk -> app rename changed the object-storage prefix used by the
serving layer (``AppFileManager.prefix``) from ``desks/{id}/`` to ``apps/{id}/``.
Each app release stores a *relative* ``dist_root_path`` (e.g.
``releases/<ver>/dist/``), so the leading prefix is what moved. The DB rows were
renamed by migration, but the **stored objects were not** — so apps deployed
before the rename 404 with ``App index.html not found`` / ``APP_NOT_FOUND``: the
serving reads ``apps/{id}/releases/.../index.html`` while the bytes still live at
``desks/{id}/releases/.../index.html``.

This script copies every object under ``desks/`` to the matching ``apps/`` path,
in the same storage backend the running service uses (GCS bucket or the local
``<local_file_storage_root>/common`` dir). It is idempotent and, by default, does
**not** overwrite objects already present under ``apps/`` (so an app re-deployed
after the rename is left alone) and does **not** delete the originals.

Run it inside the backend container (it reads the same settings/env):

    # dev (kubectl): exec into the backend pod in the lemma-dev namespace
    kubectl -n lemma-dev exec de/<backend-deployment> -c <backend-container> -- \
        python scripts/migrate_desk_assets_to_app_prefix.py --dry-run
    # then for real:
    kubectl -n lemma-dev exec de/<backend-deployment> -c <backend-container> -- \
        python scripts/migrate_desk_assets_to_app_prefix.py
    # (prod: same command, after the release that ships the rename.)

Flags:
    --dry-run         list what would be copied, change nothing
    --force           overwrite objects that already exist under apps/
    --delete-source   delete each desks/ object after a successful copy (a move)
    --app-id <uuid>   limit to a single app: only desks/<uuid>/...
    --backend gcs|local   override auto-detection
    --bucket <name>       override the GCS bucket
    --local-root <path>   override local_file_storage_root
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import obstore as obs
from obstore.exceptions import NotFoundError as ObstoreNotFoundError
from obstore.store import GCSStore, LocalStore

OLD_PREFIX = "desks/"
NEW_PREFIX = "apps/"


def _resolve_storage(args) -> tuple[str, str | None, str | None]:
    """Return (backend, bucket, local_common_dir) using the service settings,
    with optional CLI overrides."""
    bucket = args.bucket
    local_root = args.local_root
    backend = args.backend

    if backend is None or bucket is None or local_root is None:
        try:
            from app.core.config import settings  # same resolution the service uses
        except Exception as exc:  # pragma: no cover - container import guard
            print(
                "Could not import app.core.config.settings; run inside the backend "
                "(or pass --backend/--bucket/--local-root explicitly). "
                f"Import error: {exc}",
                file=sys.stderr,
            )
            raise SystemExit(2)
        backend = backend or settings.effective_storage_backend()
        bucket = bucket or settings.gcs_storage_bucket
        local_root = local_root or settings.local_file_storage_root

    if backend == "gcs":
        if not bucket:
            print("backend=gcs but no bucket configured", file=sys.stderr)
            raise SystemExit(2)
        return "gcs", bucket, None
    common = str(Path(local_root) / "common")
    return "local", None, common


def _build_root_store(backend: str, bucket: str | None, common_dir: str | None):
    """A store rooted at the bucket / common dir (NO app prefix) so we can address
    both ``desks/...`` and ``apps/...``."""
    if backend == "gcs":
        return GCSStore(bucket=bucket)
    return LocalStore(prefix=common_dir, mkdir=True)


def _list_paths(store, prefix: str) -> list[str]:
    paths: list[str] = []
    for chunk in store.list(prefix=prefix):
        paths.extend(item["path"] for item in chunk)
    return paths


async def _copy_object(store, src: str, dst: str) -> None:
    """Server-side copy when the backend supports it (GCS rewrite — no bytes through
    this process); fall back to download+upload otherwise (e.g. local store)."""
    try:
        await obs.copy_async(store, src, dst, overwrite=True)
    except (NotImplementedError, AttributeError, TypeError):
        result = await obs.get_async(store, src)
        data = (await result.bytes_async()).to_bytes()
        await obs.put_async(store, dst, data)


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="overwrite existing apps/ objects")
    parser.add_argument("--delete-source", action="store_true", help="delete desks/ object after copy")
    parser.add_argument("--app-id", default=None, help="limit to a single app id (desks/<uuid>/)")
    parser.add_argument("--concurrency", type=int, default=32, help="parallel copies")
    parser.add_argument("--backend", choices=["gcs", "local"], default=None)
    parser.add_argument("--bucket", default=None)
    parser.add_argument("--local-root", default=None)
    args = parser.parse_args()

    backend, bucket, common_dir = _resolve_storage(args)
    store = _build_root_store(backend, bucket, common_dir)
    src_prefix = OLD_PREFIX + (f"{args.app_id}/" if args.app_id else "")

    print(f"storage backend = {backend}", f"({bucket or common_dir})")
    print(f"scanning prefix = {src_prefix}")

    sources = _list_paths(store, src_prefix)
    if not sources:
        print("nothing to migrate — no objects under desks/. Done.")
        return

    existing_apps: set[str] = set()
    if not args.force:
        existing_apps = set(_list_paths(store, NEW_PREFIX + (f"{args.app_id}/" if args.app_id else "")))

    todo: list[tuple[str, str]] = []
    skipped = 0
    for src in sources:
        dst = NEW_PREFIX + src[len(OLD_PREFIX):]
        if dst in existing_apps and not args.force:
            skipped += 1
            continue
        todo.append((src, dst))

    if args.dry_run:
        for src, dst in todo:
            print(f"COPY  {src}  ->  {dst}")
        copied, deleted, errors = len(todo), 0, 0
    else:
        copied = deleted = errors = 0
        sem = asyncio.Semaphore(args.concurrency)
        counters = {"copied": 0, "deleted": 0, "errors": 0}

        async def _do(src: str, dst: str) -> None:
            async with sem:
                try:
                    await _copy_object(store, src, dst)
                    counters["copied"] += 1
                    if args.delete_source:
                        try:
                            await obs.delete_async(store, src)
                            counters["deleted"] += 1
                        except ObstoreNotFoundError:
                            pass
                    if counters["copied"] % 250 == 0:
                        print(f"  …{counters['copied']}/{len(todo)} copied")
                except Exception as exc:  # keep going; report at the end
                    counters["errors"] += 1
                    print(f"FAIL  {src} -> {dst}: {exc}", file=sys.stderr)

        await asyncio.gather(*(_do(src, dst) for src, dst in todo))
        copied, deleted, errors = counters["copied"], counters["deleted"], counters["errors"]

    print(
        f"\n{'(dry-run) ' if args.dry_run else ''}done: "
        f"{copied} copied, {skipped} skipped (already under apps/), "
        f"{deleted} source deleted, {errors} errors, {len(sources)} scanned."
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
