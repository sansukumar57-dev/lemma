"""Make the DB consistent with the desk->app / integration->connector rename.

The rename updated the code (ResourceType enum, permission ids, FlowStart fields),
but existing rows still hold pre-rename data, and old pods' system roles were never
granted the new permissions. Symptoms:

  * 403 "Missing permission app.read" listing a pod's apps — the pod's POD_VIEWER
    role has no ``app.read`` (it had ``desk.read`` only if desks existed when the
    role was seeded; many old roles never got it at all).
  * 500 ``ValueError: 'integration_application' is not a valid ResourceType`` — an
    explicit grant row still has the old ``resource_type``.
  * 500 ``FlowEntity`` validation — a workflow's ``start.config`` still has
    ``application_id`` / ``application_trigger_id``.

This single script makes everything consistent:

  1. RECONCILE system roles. For every org + pod it runs the backend's own
     ``ensure_*_system_roles`` (re-seeds the ``auth_permissions`` catalog and
     REPLACES each system role's permissions with the current code definition in
     ``SYSTEM_ROLE_PERMISSIONS``) — this is what restores ``app.read`` /
     ``connector.*`` to old roles. Idempotent: a role already correct is untouched.
  2. RENAME explicit grants (``resource_permission_grants.resource_type`` +
     ``permission_id``) that the role reconcile doesn't own (per-user / per-workload
     grants). Conflict-safe.
  3. RENAME ``workflow_flows.start.config`` keys.
  4. DROP stale ``auth_permissions`` catalog rows (old ``desk.*`` / ``integration.*``)
     once nothing references them.

Idempotent + transactional (all-or-nothing). Run ``--dry-run`` first.

    kubectl -n lemma-dev exec <backend-pod> -c lemma-api -- \
        sh -c 'cd /app/lemma-cloud && python /tmp/dbfix.py --dry-run'
    kubectl -n lemma-dev exec <backend-pod> -c lemma-api -- \
        sh -c 'cd /app/lemma-cloud && python /tmp/dbfix.py'
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from sqlalchemy import text

RESOURCE_TYPE_MAP = {
    "desk": "app",
    "integration_application": "connector",
    "integration_account": "connector_account",
    "integration_auth_config": "connector_auth_config",
}
PERMISSION_MAP = {
    "desk.read": "app.read",
    "desk.create": "app.create",
    "desk.update": "app.update",
    "desk.delete": "app.delete",
    "desk.publish": "app.publish",
    "integration.application.use": "connector.use",
    "integration.application.manage": "connector.manage",
    "integration.account.use": "connector_account.use",
    "integration.account.manage": "connector_account.manage",
    "integration.auth_config.manage": "connector_auth_config.manage",
}


async def _count(session, sql: str, params: dict | None = None) -> int:
    return (await session.execute(text(sql), params or {})).scalar() or 0


async def reconcile_system_roles(session, *, dry_run: bool, commit_every: int = 100) -> int:
    """Re-seed the permission catalog and replace every org/pod system role's
    permissions with the current code definition (adds app.read / connector.* to
    old roles). Uses the backend's own tested reconcile.

    Commits in batches (``commit_every`` pods) so prod — which may have many
    thousands of pods — never holds one giant, lock-heavy transaction. Each batch
    is independent and idempotent, so an interrupted run just resumes on re-run."""
    from app.core.authorization import service as authz_service

    authz_service._ENSURED_ROLE_SCOPES.clear()  # ignore the in-process "already ensured" cache
    svc = authz_service.AuthorizationDataService(session)

    org_ids = [r[0] for r in (await session.execute(text("SELECT id FROM organizations"))).all()]
    pods = [(r[0], r[1]) for r in (await session.execute(text("SELECT organization_id, id FROM pods"))).all()]
    print(f"  orgs: {len(org_ids)}   pods: {len(pods)}  (system-role permission sets reconciled to code)")
    if dry_run:
        return len(org_ids) + len(pods)
    for org_id in org_ids:
        await svc.ensure_org_system_roles(org_id)
    await session.commit()  # org roles + the freshly-seeded permission catalog
    for i, (org_id, pod_id) in enumerate(pods, 1):
        await svc.ensure_pod_system_roles(organization_id=org_id, pod_id=pod_id)
        if i % commit_every == 0:
            await session.commit()
            print(f"    …{i}/{len(pods)} pods committed")
    await session.commit()
    return len(org_ids) + len(pods)


async def rename_column_values(
    session, table: str, col: str, mapping: dict[str, str], peer_cols: list[str] | None, *, dry_run: bool
) -> int:
    """Rename ``col`` values per ``mapping``. ``peer_cols`` controls collisions:
    ``None`` -> plain UPDATE (column not in a unique key); ``[...]`` -> drop a stale
    row that would collide with an already-correct row (remaining unique-key cols)
    before the UPDATE (``[]`` = the column alone is the unique key, e.g. a PK)."""
    changed = 0
    for old, new in mapping.items():
        n = await _count(session, f"SELECT count(*) FROM {table} WHERE {col} = :old", {"old": old})
        if not n:
            continue
        changed += n
        print(f"  {table}.{col}: {n:>5}  {old}  ->  {new}")
        if dry_run:
            continue
        if peer_cols is not None:
            peer = " AND ".join(f"b.{c} = a.{c}" for c in peer_cols)
            peer_clause = f" AND {peer}" if peer else ""
            await session.execute(
                text(
                    f"DELETE FROM {table} a WHERE a.{col} = :old AND EXISTS "
                    f"(SELECT 1 FROM {table} b WHERE b.{col} = :new{peer_clause})"
                ),
                {"old": old, "new": new},
            )
        await session.execute(
            text(f"UPDATE {table} SET {col} = :new WHERE {col} = :old"), {"old": old, "new": new}
        )
    return changed


async def rename_flow_start_keys(session, *, dry_run: bool) -> int:
    where = "jsonb_typeof(\"start\" #> '{config}') = 'object' AND (\"start\" #> '{config}') ? :key"
    total = 0
    for old_key, new_key in (
        ("application_id", "connector_id"),
        ("application_trigger_id", "connector_trigger_id"),
    ):
        n = await _count(session, f"SELECT count(*) FROM workflow_flows WHERE {where}", {"key": old_key})
        if not n:
            continue
        total += n
        print(f"  workflow_flows.start.config: {n:>5}  {old_key}  ->  {new_key}")
        if dry_run:
            continue
        await session.execute(
            text(
                f"UPDATE workflow_flows SET \"start\" = jsonb_set("
                f"\"start\" #- '{{config,{old_key}}}', '{{config,{new_key}}}', "
                f"\"start\" #> '{{config,{old_key}}}') WHERE {where}"
            ),
            {"key": old_key},
        )
    return total


async def drop_stale_catalog_rows(session, *, dry_run: bool) -> int:
    """Delete old auth_permissions catalog rows (desk.* / integration.*) once nothing
    references them (role_permissions + grants were moved to the new ids above)."""
    old_ids = list(PERMISSION_MAP.keys())
    old_types = list(RESOURCE_TYPE_MAP.keys())
    where = (
        "(id = ANY(:ids) OR resource_type = ANY(:types)) "
        "AND NOT EXISTS (SELECT 1 FROM role_permissions r WHERE r.permission_id = auth_permissions.id) "
        "AND NOT EXISTS (SELECT 1 FROM resource_permission_grants g WHERE g.permission_id = auth_permissions.id)"
    )
    params = {"ids": old_ids, "types": old_types}
    n = await _count(session, f"SELECT count(*) FROM auth_permissions WHERE {where}", params)
    print(f"  auth_permissions (stale catalog rows to drop): {n}")
    if n and not dry_run:
        await session.execute(text(f"DELETE FROM auth_permissions WHERE {where}"), params)
    return n


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="report what would change; commit nothing")
    args = parser.parse_args()

    try:
        from app.core.infrastructure.db.session import async_session_maker
    except Exception as exc:  # pragma: no cover
        print(f"Run inside the backend (could not import the DB session): {exc}", file=sys.stderr)
        raise SystemExit(2)

    async with async_session_maker() as session:
        total = 0
        print("== 1. reconcile system roles to current code (org + pod) ==")
        total += await reconcile_system_roles(session, dry_run=args.dry_run)
        print("== 2. rename explicit grants ==")
        total += await rename_column_values(
            session, "resource_permission_grants", "resource_type", RESOURCE_TYPE_MAP,
            ["pod_id", "resource_id", "grantee_type", "grantee_id", "permission_id"], dry_run=args.dry_run,
        )
        total += await rename_column_values(
            session, "resource_permission_grants", "permission_id", PERMISSION_MAP,
            ["pod_id", "resource_type", "resource_id", "grantee_type", "grantee_id"], dry_run=args.dry_run,
        )
        print("== 3. rename workflow_flows.start ==")
        total += await rename_flow_start_keys(session, dry_run=args.dry_run)
        print("== 4. drop stale auth_permissions catalog rows ==")
        total += await drop_stale_catalog_rows(session, dry_run=args.dry_run)

        if args.dry_run:
            await session.rollback()
            print("\n(dry-run) nothing committed.")
        else:
            await session.commit()
            print("\nDone. DB is consistent with the app/connector rename.")


if __name__ == "__main__":
    asyncio.run(main())
