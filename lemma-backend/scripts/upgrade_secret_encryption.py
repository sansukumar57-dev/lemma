#!/usr/bin/env python3
"""One-shot upgrade of encrypted data to the new crypto facility (env-key based).

Use this ONCE when releasing the ``app/core/crypto`` change to an existing
deployment. It reads every encrypted value with the **old** key and rewrites it
in the new versioned ``lemma-secret-v2`` envelope under the **new** key, so old
data keeps working after the release. It is safe to re-run (idempotent) and runs
against whatever ``DATABASE_URL`` is in the environment — point it at OSS or the
cloud DB by setting that env var.

Keys (flags override env):
  --old-key   the key that encrypted existing data   (env: CONNECTOR_ENCRYPTION_KEY)
  --old-local use the local/testing dev-seed key as the old key (no value needed)
  --new-key   the key to encrypt going forward         (env: SECRET_ENCRYPTION_KEY)
              If omitted, the new key defaults to the old key — i.e. just upgrade
              the envelope format in place, no key change.

Typical release (keep the same key — recommended, lowest risk):
  1. Apply migrations (widens agent_surfaces.webhook_secret to Text).
  2. Deploy the new code keeping CONNECTOR_ENCRYPTION_KEY set (it is still read as
     a fallback). Old data already decrypts; new writes are v2 under the same key.
  3. Normalise existing rows to v2:
       PYTHONPATH=. CONNECTOR_ENCRYPTION_KEY=<key> \
         uv run python scripts/upgrade_secret_encryption.py --dry-run
       PYTHONPATH=. CONNECTOR_ENCRYPTION_KEY=<key> \
         uv run python scripts/upgrade_secret_encryption.py
  4. (Optional) Rename the env var to SECRET_ENCRYPTION_KEY (same value) and drop
     CONNECTOR_ENCRYPTION_KEY on the next deploy.

Rotating to a NEW key value at the same time:
  PYTHONPATH=. \
    CONNECTOR_ENCRYPTION_KEY=<old> SECRET_ENCRYPTION_KEY=<new> \
    uv run python scripts/upgrade_secret_encryption.py
  Keep BOTH env vars set on the running app until this completes, then drop
  CONNECTOR_ENCRYPTION_KEY.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os

from sqlalchemy import text

from app.core.crypto.cipher import EnvelopeSecretCipher
from app.core.crypto.keys import (
    derive_kid,
    is_valid_fernet_key,
    local_fallback_secret,
    LEGACY_ENV_VAR,
)
from app.core.crypto.ports import KeyMaterial, Keyring
from app.core.crypto.providers.static import StaticKeyProvider
from app.core.crypto.rotation import REGISTRY, reencrypt_all
from app.core.infrastructure.db.session import close_engine, get_session_maker


def _resolve_keys(args: argparse.Namespace) -> tuple[bytes, bytes]:
    if args.old_local:
        old = local_fallback_secret()
    else:
        raw_old = (
            args.old_key
            or os.environ.get(LEGACY_ENV_VAR)
            or os.environ.get("SECRET_ENCRYPTION_KEY")
        )
        if not raw_old:
            raise SystemExit(
                "No old key. Pass --old-key, set CONNECTOR_ENCRYPTION_KEY, or use --old-local."
            )
        old = raw_old.encode("utf-8")

    raw_new = args.new_key or os.environ.get("SECRET_ENCRYPTION_KEY")
    new = raw_new.encode("utf-8") if raw_new else old  # default: upgrade in place

    for label, key in (("old", old), ("new", new)):
        if not is_valid_fernet_key(key):
            raise SystemExit(
                f"The {label} key is not a valid Fernet key (44-char urlsafe base64)."
            )
    return old, new


def _build_cipher(old: bytes, new: bytes) -> EnvelopeSecretCipher:
    new_kid = derive_kid(new)
    keyring = Keyring(primary_kid=new_kid, keys={new_kid: KeyMaterial(new_kid, new)})
    # Read with BOTH keys (old data + any new data already written), write under new.
    legacy = [old] if old == new else [old, new]
    return EnvelopeSecretCipher(StaticKeyProvider(keyring), legacy_secrets=legacy)


async def _preflight(session, cipher: EnvelopeSecretCipher, sample: int) -> bool:
    """Verify a sample of existing rows decrypts with the old key before writing."""
    ok = True
    for col in REGISTRY:
        rows = (
            await session.execute(
                text(
                    f"SELECT id, {col.column}::text AS v FROM {col.table} "
                    f"WHERE {col.column} IS NOT NULL LIMIT :n"
                ),
                {"n": sample},
            )
        ).all()
        failures = 0
        first_error = ""
        for _id, raw in rows:
            try:
                if col.kind == "json":
                    cipher.decrypt_json(json.loads(raw))
                else:
                    cipher.decrypt_str(raw)
            except Exception as exc:  # noqa: BLE001
                failures += 1
                first_error = first_error or f"{type(exc).__name__}: {exc}"
        status = "ok" if failures == 0 else f"FAILED ({failures}/{len(rows)})"
        print(f"  preflight {col.label:40s} sampled={len(rows):<4d} {status}")
        if failures:
            ok = False
            print(f"      first error: {first_error}")
    return ok


async def _run(args: argparse.Namespace) -> int:
    old, new = _resolve_keys(args)
    cipher = _build_cipher(old, new)
    new_kid = derive_kid(new)
    print(
        f"Old key kid={derive_kid(old)}  ->  new (primary) kid={new_kid}"
        + ("  [same key: format upgrade only]" if old == new else "  [key rotation]")
    )

    session_maker = get_session_maker()
    try:
        async with session_maker() as session:
            print("\nPreflight (decrypt sample with old key):")
            if not await _preflight(session, cipher, args.sample):
                if not args.skip_preflight:
                    raise SystemExit(
                        "\nAborting: some rows did not decrypt with the old key. "
                        "Check --old-key, or pass --skip-preflight to proceed anyway."
                    )
                print("\n--skip-preflight set: continuing despite failures.")

            print("\nRe-encrypting%s:" % (" (dry-run)" if args.dry_run else ""))
            report = await reencrypt_all(
                session, cipher, batch_size=args.batch_size, dry_run=args.dry_run
            )
    finally:
        await close_engine()

    total = sum(s["migrated"] for s in report.values())
    print("\nReport%s:" % (" (dry-run)" if args.dry_run else ""))
    for label, stats in report.items():
        print(f"  {label:40s} scanned={stats['scanned']:<8d} migrated={stats['migrated']}")
    print(f"\nTotal migrated: {total}")
    if not args.dry_run and old != new:
        print(
            "\nKey was rotated. Once a re-run reports migrated=0, set "
            "SECRET_ENCRYPTION_KEY to the new key on the app and drop "
            "CONNECTOR_ENCRYPTION_KEY."
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--old-key", help="Old Fernet key (default: $CONNECTOR_ENCRYPTION_KEY)")
    parser.add_argument(
        "--old-local", action="store_true", help="Use the local/testing dev-seed as the old key"
    )
    parser.add_argument("--new-key", help="New Fernet key (default: $SECRET_ENCRYPTION_KEY or old key)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--batch-size", type=int, default=500, help="Rows per page/commit")
    parser.add_argument("--sample", type=int, default=20, help="Rows per table to preflight-check")
    parser.add_argument(
        "--skip-preflight", action="store_true", help="Proceed even if preflight decryption fails"
    )
    args = parser.parse_args(argv)
    return asyncio.run(_run(args))


if __name__ == "__main__":
    raise SystemExit(main())
