#!/usr/bin/env python3
"""Re-encrypt all secrets at rest onto the current primary key.

The operational tool for key rotation and key-compromise recovery. It walks
every encrypted column (see ``app.core.crypto.rotation.REGISTRY``), decrypts each
value with whatever key/version produced it, and re-encrypts under the configured
primary key. Idempotent: rows already under the primary key are skipped.

Routine rotation (static keyset):
    1. Add a new key to SECRET_ENCRYPTION_KEYSET with "primary": true; keep the
       old key in the set so existing data still decrypts.
    2. Deploy so the new primary is active.
    3. Run this script to re-encrypt forward.
    4. Once it reports 0 migrated on a re-run, drop the old key from the keyset.

Key compromise:
    Same as above but run with --force after rotating, then remove the leaked key
    immediately (a re-run reporting 0 migrated confirms no data is left under it).

Usage:
    PYTHONPATH=. uv run python scripts/reencrypt_secrets.py --dry-run
    PYTHONPATH=. uv run python scripts/reencrypt_secrets.py
    PYTHONPATH=. uv run python scripts/reencrypt_secrets.py --force --batch-size 1000
    PYTHONPATH=. uv run python scripts/reencrypt_secrets.py --only accounts.credentials
"""

from __future__ import annotations

import argparse
import asyncio

from app.core.crypto.factory import get_secret_cipher, reset_crypto_caches
from app.core.crypto.rotation import REGISTRY, reencrypt_all
from app.core.infrastructure.db.session import close_engine, get_session_maker


async def _run(args: argparse.Namespace) -> int:
    reset_crypto_caches()
    cipher = get_secret_cipher()

    columns = REGISTRY
    if args.only:
        columns = [c for c in REGISTRY if c.label in set(args.only)]
        if not columns:
            known = ", ".join(c.label for c in REGISTRY)
            raise SystemExit(f"No column matches {args.only}. Known: {known}")

    session_maker = get_session_maker()
    try:
        async with session_maker() as session:
            report = await reencrypt_all(
                session,
                cipher,
                force=args.force,
                batch_size=args.batch_size,
                dry_run=args.dry_run,
                columns=columns,
            )
    finally:
        await close_engine()

    print("\nRe-encryption report%s:" % (" (dry-run)" if args.dry_run else ""))
    total_migrated = 0
    for label, stats in report.items():
        total_migrated += stats["migrated"]
        print(f"  {label:40s} scanned={stats['scanned']:<8d} migrated={stats['migrated']}")
    print(f"\nTotal migrated: {total_migrated}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing anything",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-encrypt every row even if already under the primary key",
    )
    parser.add_argument(
        "--batch-size", type=int, default=500, help="Rows per page/commit (default: 500)"
    )
    parser.add_argument(
        "--only",
        action="append",
        help="Limit to specific column label(s); repeatable (e.g. accounts.credentials)",
    )
    args = parser.parse_args(argv)
    return asyncio.run(_run(args))


if __name__ == "__main__":
    raise SystemExit(main())
