"""Backfill centralized auth roles for legacy org and pod memberships.

Run from ``lemma-backend`` with the usual backend environment loaded:

    uv run python scripts/backfill_legacy_membership_roles.py --dry-run
    uv run python scripts/backfill_legacy_membership_roles.py
"""

from __future__ import annotations

import argparse
import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Row, distinct, select, tuple_, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization.models import RoleAssignmentModel, RoleModel
from app.core.authorization.service import (
    AuthorizationDataService,
    SYSTEM_ORG_ROLES,
)
from app.core.infrastructure.db.session import async_session_maker, close_engine
from app.modules.identity.infrastructure.models.organization_models import (
    OrganizationMember,
)
from app.modules.pod.infrastructure.models.pod_models import Pod, PodMember


ORG_MEMBER_PRINCIPAL = "ORG_MEMBER"
POD_MEMBER_PRINCIPAL = "POD_MEMBER"
DEFAULT_ORG_ROLE = "ORG_MEMBER"
DEFAULT_POD_ROLE = "POD_USER"
CREATOR_ORG_ROLE = "ORG_OWNER"
CREATOR_POD_ROLE = "POD_ADMIN"


@dataclass
class BackfillStats:
    pods_seen: int = 0
    org_system_scopes_ensured: int = 0
    pod_system_scopes_ensured: int = 0
    creator_org_members_inserted: int = 0
    creator_org_members_promoted: int = 0
    creator_pod_members_inserted: int = 0
    org_role_assignments_inserted: int = 0
    pod_role_assignments_inserted: int = 0
    creator_org_owner_assignments_inserted: int = 0
    creator_pod_admin_assignments_inserted: int = 0


def _count_returned(rows: Iterable[object]) -> int:
    return sum(1 for _ in rows)


def _dedupe_assignment_rows(rows: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[tuple[object, object, object]] = set()
    deduped: list[dict[str, object]] = []
    for row in rows:
        key = (row["role_id"], row["principal_type"], row["principal_id"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


async def _insert_and_count(session: AsyncSession, stmt) -> int:
    result = await session.execute(stmt)
    return _count_returned(result.all())


async def _ensure_system_roles(
    session: AsyncSession,
    pods: list[Row],
    stats: BackfillStats,
) -> None:
    authz = AuthorizationDataService(session)
    org_ids = set(
        (
            await session.execute(
                select(distinct(OrganizationMember.organization_id))
            )
        ).scalars()
    )
    org_ids.update(pod.organization_id for pod in pods)

    for org_id in sorted(org_ids, key=str):
        await authz.ensure_org_system_roles(org_id)
        stats.org_system_scopes_ensured += 1

    for pod in pods:
        await authz.ensure_pod_system_roles(
            organization_id=pod.organization_id,
            pod_id=pod.id,
        )
        stats.pod_system_scopes_ensured += 1


async def _fetch_pods(session: AsyncSession, *, include_deleted: bool) -> list[Row]:
    stmt = select(Pod.id, Pod.organization_id, Pod.user_id)
    if not include_deleted:
        stmt = stmt.where(Pod.is_deleted.is_(False))
    return list((await session.execute(stmt)).all())


async def _upsert_creator_memberships(
    session: AsyncSession,
    pods: list[Row],
    stats: BackfillStats,
) -> dict[tuple[UUID, UUID], UUID]:
    creator_pairs = sorted(
        {(pod.user_id, pod.organization_id) for pod in pods},
        key=lambda item: (str(item[1]), str(item[0])),
    )
    if not creator_pairs:
        return {}

    creator_org_member_rows = [
        {
            "user_id": user_id,
            "organization_id": organization_id,
            "role": CREATOR_ORG_ROLE,
        }
        for user_id, organization_id in creator_pairs
    ]
    stats.creator_org_members_inserted = await _insert_and_count(
        session,
        pg_insert(OrganizationMember)
        .values(creator_org_member_rows)
        .on_conflict_do_nothing(
            index_elements=["user_id", "organization_id"],
        )
        .returning(OrganizationMember.id),
    )

    promoted = await session.execute(
        update(OrganizationMember)
        .where(
            tuple_(
                OrganizationMember.user_id,
                OrganizationMember.organization_id,
            ).in_(creator_pairs),
            OrganizationMember.role != CREATOR_ORG_ROLE,
        )
        .values(role=CREATOR_ORG_ROLE)
        .returning(OrganizationMember.id)
    )
    stats.creator_org_members_promoted = _count_returned(promoted.all())

    org_members = list(
        (
            await session.execute(
                select(
                    OrganizationMember.id,
                    OrganizationMember.user_id,
                    OrganizationMember.organization_id,
                ).where(
                    tuple_(
                        OrganizationMember.user_id,
                        OrganizationMember.organization_id,
                    ).in_(creator_pairs),
                )
            )
        ).all()
    )
    creator_org_member_ids = {
        (row.user_id, row.organization_id): row.id for row in org_members
    }

    pod_member_rows = [
        {
            "pod_id": pod.id,
            "organization_member_id": creator_org_member_ids[
                (pod.user_id, pod.organization_id)
            ],
        }
        for pod in pods
    ]
    stats.creator_pod_members_inserted = await _insert_and_count(
        session,
        pg_insert(PodMember)
        .values(pod_member_rows)
        .on_conflict_do_nothing(
            index_elements=["pod_id", "organization_member_id"],
        )
        .returning(PodMember.id),
    )

    return creator_org_member_ids


async def _load_roles(
    session: AsyncSession,
) -> dict[tuple[UUID, UUID | None, str], UUID]:
    role_rows = (
        await session.execute(
            select(RoleModel.id, RoleModel.organization_id, RoleModel.pod_id, RoleModel.name)
        )
    ).all()
    return {
        (row.organization_id, row.pod_id, row.name): row.id
        for row in role_rows
    }


async def _assign_org_roles(
    session: AsyncSession,
    role_ids: dict[tuple[UUID, UUID | None, str], UUID],
    stats: BackfillStats,
) -> None:
    org_members = (
        await session.execute(
            select(
                OrganizationMember.id,
                OrganizationMember.organization_id,
                OrganizationMember.role,
            )
        )
    ).all()
    rows = []
    for member in org_members:
        role_name = member.role if member.role in SYSTEM_ORG_ROLES else DEFAULT_ORG_ROLE
        role_id = role_ids.get((member.organization_id, None, role_name))
        if role_id is None:
            continue
        rows.append(
            {
                "role_id": role_id,
                "principal_type": ORG_MEMBER_PRINCIPAL,
                "principal_id": member.id,
            }
        )
    rows = _dedupe_assignment_rows(rows)
    if not rows:
        return
    stats.org_role_assignments_inserted = await _insert_and_count(
        session,
        pg_insert(RoleAssignmentModel)
        .values(rows)
        .on_conflict_do_nothing(
            constraint="uq_role_assignments_role_principal",
        )
        .returning(RoleAssignmentModel.id),
    )


async def _assign_pod_user_roles(
    session: AsyncSession,
    role_ids: dict[tuple[UUID, UUID | None, str], UUID],
    stats: BackfillStats,
) -> None:
    pod_members = (
        await session.execute(
            select(
                PodMember.id,
                PodMember.pod_id,
                Pod.organization_id,
            ).join(Pod, Pod.id == PodMember.pod_id)
        )
    ).all()
    rows = []
    for member in pod_members:
        role_id = role_ids.get((member.organization_id, member.pod_id, DEFAULT_POD_ROLE))
        if role_id is None:
            continue
        rows.append(
            {
                "role_id": role_id,
                "principal_type": POD_MEMBER_PRINCIPAL,
                "principal_id": member.id,
            }
        )
    rows = _dedupe_assignment_rows(rows)
    if not rows:
        return
    stats.pod_role_assignments_inserted = await _insert_and_count(
        session,
        pg_insert(RoleAssignmentModel)
        .values(rows)
        .on_conflict_do_nothing(
            constraint="uq_role_assignments_role_principal",
        )
        .returning(RoleAssignmentModel.id),
    )


async def _assign_creator_elevated_roles(
    session: AsyncSession,
    pods: list[Row],
    role_ids: dict[tuple[UUID, UUID | None, str], UUID],
    stats: BackfillStats,
) -> None:
    if not pods:
        return
    creator_pairs = {(pod.user_id, pod.organization_id) for pod in pods}
    creator_members = (
        await session.execute(
            select(
                OrganizationMember.id,
                OrganizationMember.user_id,
                OrganizationMember.organization_id,
            ).where(
                tuple_(
                    OrganizationMember.user_id,
                    OrganizationMember.organization_id,
                ).in_(creator_pairs),
            )
        )
    ).all()
    creator_org_member_by_pair = {
        (row.user_id, row.organization_id): row.id
        for row in creator_members
    }

    org_rows = []
    pod_rows = []
    for pod in pods:
        org_member_id = creator_org_member_by_pair.get((pod.user_id, pod.organization_id))
        if org_member_id is None:
            continue
        org_owner_role_id = role_ids.get((pod.organization_id, None, CREATOR_ORG_ROLE))
        if org_owner_role_id is not None:
            org_rows.append(
                {
                    "role_id": org_owner_role_id,
                    "principal_type": ORG_MEMBER_PRINCIPAL,
                    "principal_id": org_member_id,
                }
            )

        pod_member_id = (
            await session.execute(
                select(PodMember.id).where(
                    PodMember.pod_id == pod.id,
                    PodMember.organization_member_id == org_member_id,
                )
            )
        ).scalar_one_or_none()
        pod_admin_role_id = role_ids.get((pod.organization_id, pod.id, CREATOR_POD_ROLE))
        if pod_member_id is not None and pod_admin_role_id is not None:
            pod_rows.append(
                {
                    "role_id": pod_admin_role_id,
                    "principal_type": POD_MEMBER_PRINCIPAL,
                    "principal_id": pod_member_id,
                }
            )

    org_rows = _dedupe_assignment_rows(org_rows)
    pod_rows = _dedupe_assignment_rows(pod_rows)
    if org_rows:
        stats.creator_org_owner_assignments_inserted = await _insert_and_count(
            session,
            pg_insert(RoleAssignmentModel)
            .values(org_rows)
            .on_conflict_do_nothing(
                constraint="uq_role_assignments_role_principal",
            )
            .returning(RoleAssignmentModel.id),
        )
    if pod_rows:
        stats.creator_pod_admin_assignments_inserted = await _insert_and_count(
            session,
            pg_insert(RoleAssignmentModel)
            .values(pod_rows)
            .on_conflict_do_nothing(
                constraint="uq_role_assignments_role_principal",
            )
            .returning(RoleAssignmentModel.id),
        )


async def backfill(*, dry_run: bool, include_deleted: bool) -> BackfillStats:
    async with async_session_maker() as session:
        stats = BackfillStats()
        pods = await _fetch_pods(session, include_deleted=include_deleted)
        stats.pods_seen = len(pods)

        await _ensure_system_roles(session, pods, stats)
        await _upsert_creator_memberships(session, pods, stats)
        role_ids = await _load_roles(session)
        await _assign_org_roles(session, role_ids, stats)
        await _assign_pod_user_roles(session, role_ids, stats)
        await _assign_creator_elevated_roles(session, pods, role_ids, stats)

        if dry_run:
            await session.rollback()
        else:
            await session.commit()
        return stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill missing org/pod role assignments for legacy memberships.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the backfill inside a transaction and roll it back.",
    )
    parser.add_argument(
        "--include-deleted",
        action="store_true",
        help="Also process pods marked is_deleted=true.",
    )
    return parser.parse_args()


def print_stats(stats: BackfillStats, *, dry_run: bool) -> None:
    mode = "DRY RUN - rolled back" if dry_run else "APPLIED"
    print(f"Legacy membership role backfill complete ({mode}).")
    for field, value in stats.__dict__.items():
        print(f"{field}: {value}")


async def main() -> None:
    args = parse_args()
    try:
        stats = await backfill(
            dry_run=args.dry_run,
            include_deleted=args.include_deleted,
        )
        print_stats(stats, dry_run=args.dry_run)
    finally:
        await close_engine()


if __name__ == "__main__":
    asyncio.run(main())
