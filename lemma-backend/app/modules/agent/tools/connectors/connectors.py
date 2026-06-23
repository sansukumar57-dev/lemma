from __future__ import annotations

import traceback
from collections.abc import Awaitable, Callable

from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent as PydanticAIAgent
from pydantic_ai.exceptions import ModelRetry
from pydantic_ai.tools import RunContext
from pydantic_ai.toolsets import FunctionToolset

from app.core.infrastructure.db.session import async_session_maker
from app.core.infrastructure.db.uow import SqlAlchemyUnitOfWork
from app.modules.agent.tools.context import get_prompt
from app.modules.agent.tools.connectors.models import (
    ConnectorHelperAgentOutput,
    ConnectorHelperAgentRequest,
    ConnectorHelperAgentResponse,
)
from app.modules.connectors.api.dependencies import build_connector_operation_service
from app.modules.connectors.api.schemas.connector_operation_schemas import (
    OperationDetailsBatchResponse,
    OperationDiscoverResponse,
)
from app.modules.connectors.services.connector_operation_service import (
    ConnectorOperationService,
)
from app.core.infrastructure.events.message_bus import get_message_bus
from app.core.log.log import get_logger
from app.modules.agent.services.runtime_model_factory import (
    default_system_runtime,
    require_pydantic_ai_model_from_runtime_profile,
)
from app.modules.usage.services.pydantic_ai_tracking import (
    record_pydantic_ai_result_usage,
    reserve_usage_for_runtime,
)
from app.modules.usage.services.usage_context import current_usage_context

logger = get_logger(__name__)


class _ConnectorInfoToolDeps(BaseModel):
    allowed_app_names: list[str]
    service: ConnectorOperationService | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class _OperationSearchToolRequest(BaseModel):
    connector_id: str
    query: str | None = None
    limit: int | None = None


class _OperationDetailsToolRequest(BaseModel):
    connector_id: str
    operation_names: list[str] | None = None


def _ensure_app_allowed(
    allowed_app_names: list[str],
    connector_id: str,
) -> None:
    # Raise ModelRetry (not ValueError) so the helper sub-agent gets a corrective
    # message and can re-issue against an allowed app, instead of aborting the run.
    if connector_id not in allowed_app_names:
        allowed = ", ".join(allowed_app_names) or "(none)"
        raise ModelRetry(
            f"Connector '{connector_id}' is not allowed for this helper call. "
            f"Allowed connectors: {allowed}."
        )


async def search_operations_tool(
    ctx: RunContext[_ConnectorInfoToolDeps],
    request: _OperationSearchToolRequest,
) -> OperationDiscoverResponse:
    """Search operations for one connector using only name and description."""

    _ensure_app_allowed(ctx.deps.allowed_app_names, request.connector_id)
    return await _with_connector_operation_service(
        ctx.deps,
        lambda service: service.discover_operations(
            request.connector_id,
            query=request.query,
            limit=request.limit,
        ),
    )


async def get_operation_details_tool(
    ctx: RunContext[_ConnectorInfoToolDeps],
    request: _OperationDetailsToolRequest,
) -> OperationDetailsBatchResponse:
    """Fetch detailed input and output schemas for one or more operations."""

    _ensure_app_allowed(ctx.deps.allowed_app_names, request.connector_id)
    return await _with_connector_operation_service(
        ctx.deps,
        lambda service: service.get_operation_details_batch(
            request.connector_id,
            operation_names=request.operation_names,
        ),
    )


async def _with_connector_operation_service(
    deps: _ConnectorInfoToolDeps,
    callback: Callable[
        [ConnectorOperationService],
        Awaitable[OperationDiscoverResponse | OperationDetailsBatchResponse],
    ],
) -> OperationDiscoverResponse | OperationDetailsBatchResponse:
    if deps.service is not None:
        return await callback(deps.service)

    async with async_session_maker() as session:
        uow = SqlAlchemyUnitOfWork(session, message_bus=get_message_bus())
        service = build_connector_operation_service(uow)
        return await callback(service)


connector_info_toolset = FunctionToolset[_ConnectorInfoToolDeps](
    tools=[
        search_operations_tool,
        get_operation_details_tool,
    ]
)


async def connector_helper_agent_internal(
    request: ConnectorHelperAgentRequest,
    service: ConnectorOperationService | None = None,
) -> ConnectorHelperAgentResponse:
    """Plan connector usage for a goal by discovering and inspecting operations."""

    try:
        prompt = await get_prompt("connector_helper_agent")
        resolved_runtime = await default_system_runtime()
        runtime_profile = resolved_runtime.public_snapshot()
        model = require_pydantic_ai_model_from_runtime_profile(
            runtime_profile=runtime_profile,
            runtime_credentials=resolved_runtime.credentials or {},
            fallback_model_name=resolved_runtime.model_name_for_harness,
        )
        agent = PydanticAIAgent(
            model,
            instructions=prompt,
            toolsets=[connector_info_toolset],
            output_type=ConnectorHelperAgentOutput,
        )
        normalized_app_names = [
            app_name.strip() for app_name in request.app_names if app_name.strip()
        ]
        deps = _ConnectorInfoToolDeps(
            allowed_app_names=normalized_app_names,
            service=service,
        )
        user_prompt = (
            f"Goal:\n{request.goal}\n\n"
            f"Allowed connectors: {', '.join(normalized_app_names)}\n"
            "Use the search and details tools before making recommendations."
        )
        usage_context = current_usage_context()
        usage_reservation = None
        if usage_context is not None:
            usage_reservation = await reserve_usage_for_runtime(
                organization_id=usage_context.organization_id,
                user_id=usage_context.user_id,
                runtime_profile=runtime_profile,
            )
        result = None
        try:
            result = await agent.run(user_prompt, deps=deps)
            if usage_context is not None:
                await record_pydantic_ai_result_usage(
                    ctx=usage_context,
                    runtime_profile=runtime_profile,
                    result=result,
                    status="COMPLETED",
                    reservation=usage_reservation,
                    metadata={"helper": "connector_helper_agent"},
                )
        except Exception:
            if usage_context is not None:
                await record_pydantic_ai_result_usage(
                    ctx=usage_context,
                    runtime_profile=runtime_profile,
                    result=result,
                    status="FAILED",
                    reservation=usage_reservation,
                    metadata={"helper": "connector_helper_agent"},
                )
            raise
        return ConnectorHelperAgentResponse(
            success=True,
            answer_markdown=result.output.answer_markdown,
            operations_by_app=result.output.operations_by_app,
            message="Connector helper completed successfully.",
        )
    except Exception as exc:
        logger.error(
            "Error in connector helper agent: %s, traceback: %s",
            exc,
            traceback.format_exc(),
        )
        return ConnectorHelperAgentResponse(
            success=False,
            error=str(exc),
            message="Connector helper failed.",
        )
