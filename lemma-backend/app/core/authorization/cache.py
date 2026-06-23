"""In-process authorization role snapshot cache."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from uuid import UUID

from app.core.authorization.context import PrincipalRef
from app.core.config import settings


@dataclass(frozen=True, slots=True)
class RoleSnapshot:
    organization_id: UUID | None
    pod_id: UUID | None
    role_ids: frozenset[UUID]
    role_names: frozenset[str]
    permission_ids: frozenset[str]
    principal_refs: frozenset[PrincipalRef]
    grant_principal_sets: tuple[frozenset[PrincipalRef], ...]


_ROLE_SNAPSHOT_CACHE: dict[
    tuple[UUID, UUID | None, UUID | None],
    tuple[float, RoleSnapshot],
] = {}


def get_role_snapshot(
    *,
    user_id: UUID,
    organization_id: UUID | None,
    pod_id: UUID | None,
) -> RoleSnapshot | None:
    ttl = settings.authorization_role_cache_ttl_seconds
    if ttl <= 0:
        return None
    key = (user_id, organization_id, pod_id)
    cached = _ROLE_SNAPSHOT_CACHE.get(key)
    if cached is None:
        return None
    expires_at, snapshot = cached
    if expires_at <= monotonic():
        _ROLE_SNAPSHOT_CACHE.pop(key, None)
        return None
    return snapshot


def set_role_snapshot(
    *,
    user_id: UUID,
    snapshot: RoleSnapshot,
) -> None:
    ttl = settings.authorization_role_cache_ttl_seconds
    if ttl <= 0:
        return
    key = (user_id, snapshot.organization_id, snapshot.pod_id)
    _ROLE_SNAPSHOT_CACHE[key] = (monotonic() + ttl, snapshot)


def invalidate_role_snapshot_cache(
    *,
    organization_id: UUID | None = None,
    pod_id: UUID | None = None,
    user_id: UUID | None = None,
) -> None:
    if organization_id is None and pod_id is None and user_id is None:
        _ROLE_SNAPSHOT_CACHE.clear()
        return
    for cached_user_id, cached_org_id, cached_pod_id in list(_ROLE_SNAPSHOT_CACHE):
        if user_id is not None and cached_user_id != user_id:
            continue
        if organization_id is not None and cached_org_id != organization_id:
            continue
        if pod_id is not None and cached_pod_id != pod_id:
            continue
        _ROLE_SNAPSHOT_CACHE.pop((cached_user_id, cached_org_id, cached_pod_id), None)
