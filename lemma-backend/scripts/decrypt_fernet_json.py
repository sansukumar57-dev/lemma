#!/usr/bin/env python3
"""Decrypt a Lemma encrypted-JSON payload back into plaintext JSON.

Reads both envelope versions written by the crypto facility
(`app/core/crypto`):

    # legacy v1
    {"_encrypted": "fernet-json-v1", "ciphertext": "<token>"}

    # v2 (local fernet alg)
    {"_encrypted": "lemma-secret-v2", "kid": "...", "alg": "fernet", "ct": "<b64>"}

v2 `alg: "kms+fernet"` envelopes cannot be decrypted here — the data key is
wrapped by Cloud KMS; use a context with KMS access instead.

The Fernet key is the raw urlsafe-base64 key string (passed straight to
`Fernet(...)`, exactly as the cipher does with `key.encode("utf-8")`).

Usage:
    # key from a CLI arg
    python scripts/decrypt_fernet_json.py --key "<fernet-key>" payload.json

    # key from an env var (avoids it landing in shell history)
    CONNECTOR_ENCRYPTION_KEY=<fernet-key> \
        python scripts/decrypt_fernet_json.py payload.json

    # local/testing default key (matches the adapter's dev fallback)
    python scripts/decrypt_fernet_json.py --local payload.json

    # write to a file instead of stdout
    python scripts/decrypt_fernet_json.py --key "<key>" payload.json -o out.json
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

V1_MARKER = "fernet-json-v1"
V2_MARKER = "lemma-secret-v2"
# Matches the crypto facility's local/testing fallback key seed.
LOCAL_KEY_SEED = b"lemma-local-connector-secret-key"


def _local_key() -> bytes:
    digest = hashlib.sha256(LOCAL_KEY_SEED).digest()
    return base64.urlsafe_b64encode(digest)


def _resolve_key(args: argparse.Namespace) -> bytes:
    if args.local:
        return _local_key()
    key = args.key or os.environ.get("CONNECTOR_ENCRYPTION_KEY")
    if not key:
        raise SystemExit(
            "No key provided. Pass --key, set CONNECTOR_ENCRYPTION_KEY, or use --local."
        )
    return key.encode("utf-8")


def decrypt_payload(payload: dict[str, Any], fernet: Fernet) -> Any:
    """Decrypt a single v1/v2 envelope; return non-encrypted values unchanged."""
    marker = payload.get("_encrypted")
    if marker == V1_MARKER:
        token = payload.get("ciphertext")
        if not isinstance(token, str):
            raise ValueError("Encrypted JSON payload is missing a string 'ciphertext'")
        plaintext = fernet.decrypt(token.encode("ascii"))
        return json.loads(plaintext.decode("utf-8"))
    if marker == V2_MARKER:
        alg = payload.get("alg")
        if alg != "fernet":
            raise SystemExit(
                f"Cannot decrypt v2 envelope with alg={alg!r} here "
                "(kms+fernet needs Cloud KMS access)."
            )
        ct = payload.get("ct")
        if not isinstance(ct, str):
            raise ValueError("v2 envelope is missing a string 'ct'")
        plaintext = fernet.decrypt(base64.urlsafe_b64decode(ct.encode("ascii")))
        return json.loads(plaintext.decode("utf-8"))
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("payload", type=Path, help="Path to the JSON file holding the encrypted envelope")
    parser.add_argument("--key", help="Fernet key (urlsafe base64). Defaults to $CONNECTOR_ENCRYPTION_KEY")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Use the local/testing fallback key derived from the dev seed",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write decrypted JSON here instead of stdout",
    )
    parser.add_argument("--indent", type=int, default=2, help="Indent for output JSON (default: 2)")
    args = parser.parse_args(argv)

    fernet = Fernet(_resolve_key(args))

    raw = json.loads(args.payload.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise SystemExit("Payload file must contain a JSON object envelope")

    try:
        decrypted = decrypt_payload(raw, fernet)
    except InvalidToken:
        raise SystemExit(
            "Decryption failed (InvalidToken): the key does not match this ciphertext."
        )

    rendered = json.dumps(decrypted, indent=args.indent, sort_keys=True, ensure_ascii=False)

    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote decrypted JSON to {args.output}", file=sys.stderr)
    else:
        print(rendered)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
