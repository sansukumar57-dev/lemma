from __future__ import annotations

import time
from typing import Any


class TTLCache:
    """Minimal in-process TTL cache for small metadata lookups (tokens,
    OIDC documents, consent checks)."""

    def __init__(self) -> None:
        self._entries: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if expires_at <= time.monotonic():
            self._entries.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any, *, ttl_seconds: float) -> None:
        self._entries[key] = (time.monotonic() + ttl_seconds, value)

    def clear(self) -> None:
        self._entries.clear()
