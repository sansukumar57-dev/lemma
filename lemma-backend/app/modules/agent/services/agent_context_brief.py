"""Builds the runtime-context brief appended to an agent's system prompt.

The brief grounds the agent in its environment without it having to run any
discovery commands: the current pod, the current user, and the resources it can
work with — for the pod default assistant the full pod inventory (a server-side
``pod describe``), for a user-created agent only the resources granted to it,
each with name, description, and (for tables) schema.
"""

from __future__ import annotations

from uuid import UUID

from app.core.authorization.context import ResourceType
from app.core.authorization.current import reset_current_context, set_current_context
from app.core.authorization.delegation import DEFAULT_POD_AGENT_ID
from app.core.infrastructure.db.uow_factory import UnitOfWorkFactory
from app.modules.agent.domain.entities import Agent, Conversation
from app.modules.agent.infrastructure.context_brief_repository import (
    AgentContextBriefRepository,
)
from app.modules.agent.infrastructure.repositories import AgentRepository
from app.modules.datastore.api.dependencies import (
    build_file_service,
    build_table_service,
)
from app.modules.function.infrastructure.repositories import FunctionRepository
from app.modules.pod.services.authorization_factory import create_authorization_service

_MAX_TABLES = 50
_MAX_RESOURCES = 50
_MAX_COLUMNS = 40


class AgentContextBriefBuilder:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def build(
        self,
        *,
        agent: Agent,
        conversation: Conversation,
        user_id: UUID,
        pod_id: UUID,
    ) -> str:
        async with self.uow_factory() as uow:
            repo = AgentContextBriefRepository(uow)
            pod_name = await repo.get_pod_name(pod_id) or "(unknown)"
            email = await repo.get_user_email(user_id)
            user_line = f"{email} ({user_id})" if email else str(user_id)

            lines = [
                "# Runtime Context",
                f"- Pod: {pod_name} ({pod_id})",
                f"- User: {user_line}",
            ]

            # The pod default assistant runs with the user's permissions and sees
            # the whole pod; named agents see only what they're granted.
            is_default = (
                conversation.is_pod_assistant or agent.id == DEFAULT_POD_AGENT_ID
            )
            auth_ctx = await create_authorization_service(uow).build_user_context(
                user_id=user_id,
                pod_id=pod_id,
            )
            token = set_current_context(auth_ctx)
            try:
                if is_default:
                    lines.extend(
                        await self._pod_inventory(uow, auth_ctx, pod_id)
                    )
                else:
                    lines.extend(
                        await self._granted_resources(uow, auth_ctx, agent, pod_id)
                    )
            finally:
                reset_current_context(token)

        return "\n".join(lines)

    async def _pod_inventory(self, uow, ctx, pod_id: UUID) -> list[str]:
        lines: list[str] = []
        table_service = build_table_service(uow)
        tables, _ = await table_service.list_tables(pod_id, ctx, limit=_MAX_TABLES)
        if tables:
            lines.append("\n## Tables")
            lines.extend(_table_line(table) for table in tables)

        agents, _ = await AgentRepository(uow).list_by_pod(
            pod_id=pod_id, limit=_MAX_RESOURCES
        )
        named = [a for a in agents if a.id != DEFAULT_POD_AGENT_ID]
        if named:
            lines.append("\n## Agents")
            lines.extend(
                f"- {a.name}" + (f" — {a.description}" if a.description else "")
                for a in named
            )

        functions, _ = await FunctionRepository(uow).list_by_pod(
            pod_id, limit=_MAX_RESOURCES
        )
        if functions:
            lines.append("\n## Functions")
            lines.extend(
                f"- {f.name} [{f.type.value if hasattr(f.type, 'value') else f.type}]"
                + (f" — {f.description}" if f.description else "")
                for f in functions
            )

        try:
            tree = await build_file_service(uow).get_directory_tree(
                pod_id, ctx, root_path="/", files_per_directory=5
            )
            entries = _top_level_file_entries(tree)
            if entries:
                lines.append("\n## Files (top level)")
                lines.extend(f"- {entry}" for entry in entries)
        except Exception:
            # Files are best-effort context; never fail prompt assembly on them.
            pass
        return lines

    async def _granted_resources(self, uow, ctx, agent: Agent, pod_id: UUID) -> list[str]:
        repo = AgentContextBriefRepository(uow)
        rows = await repo.get_agent_grants(pod_id=pod_id, agent_id=agent.id)
        if not rows:
            return ["\n## Granted Resources\n- (none)"]

        refs: list[tuple[ResourceType, UUID]] = []
        perms_by_ref: dict[tuple[str, UUID], set[str]] = {}
        for resource_type, resource_id, permission_id in rows:
            try:
                ref_type = ResourceType(resource_type)
            except ValueError:
                continue
            refs.append((ref_type, resource_id))
            perms_by_ref.setdefault((resource_type, resource_id), set()).add(
                permission_id
            )
        names = await repo.resolve_resource_names(pod_id=pod_id, refs=refs)

        # Granted table schemas (resolve names -> column summaries).
        granted_table_names = {
            names.get((ResourceType.DATASTORE_TABLE, rid))
            for (rtype, rid) in {(r[0], r[1]) for r in rows}
            if rtype == "datastore_table"
        }
        granted_table_names.discard(None)
        table_summaries: dict[str, str] = {}
        if granted_table_names:
            tables, _ = await build_table_service(uow).list_tables(
                pod_id, ctx, limit=_MAX_TABLES
            )
            for table in tables:
                if table.table_name in granted_table_names:
                    table_summaries[table.table_name] = _table_line(table)

        lines = ["\n## Granted Resources"]
        for (resource_type, resource_id), perms in list(perms_by_ref.items())[
            :_MAX_RESOURCES
        ]:
            try:
                ref_type = ResourceType(resource_type)
            except ValueError:
                continue
            name = names.get((ref_type, resource_id))
            if name is None:
                continue
            perm_list = ", ".join(sorted(perms))
            if resource_type == "datastore_table" and name in table_summaries:
                lines.append(f"{table_summaries[name]}  (grants: {perm_list})")
            else:
                lines.append(f"- {resource_type}: {name}  (grants: {perm_list})")
        return lines


def _table_line(table) -> str:
    columns = ", ".join(
        f"{c.name}:{c.type.value if hasattr(c.type, 'value') else c.type}"
        for c in table.columns[:_MAX_COLUMNS]
    )
    return f"- {table.table_name} (pk: {table.primary_key_column}): {columns}"


def _top_level_file_entries(tree: object) -> list[str]:
    if not isinstance(tree, dict):
        return []
    children = tree.get("children")
    if not isinstance(children, list):
        return []
    entries: list[str] = []
    for child in children[:_MAX_RESOURCES]:
        if isinstance(child, dict):
            name = child.get("path") or child.get("name")
            kind = child.get("kind") or child.get("type")
            if name:
                entries.append(f"{name}" + (f" [{kind}]" if kind else ""))
    return entries
