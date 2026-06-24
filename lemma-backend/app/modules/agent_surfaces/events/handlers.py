from __future__ import annotations

import logging
from typing import AsyncGenerator

from faststream import Depends, Logger
from faststream.redis import RedisRouter

from app.core.infrastructure.db.session import async_session_maker
from app.core.infrastructure.db.uow import SqlAlchemyUnitOfWork
from app.core.infrastructure.db.uow_factory import (
    create_uow_from_session_maker,
)
from app.core.infrastructure.events.stream_subscriber import redis_stream_sub
from app.core.infrastructure.jobs.streaq_job_queue import (
    SharedStreaqJobQueue,
    get_streaq_job_queue,
)
from app.core.infrastructure.jobs.streaq_runtime import AppWorkerContext, streaq_task, streaq_worker
from app.modules.agent.api.dependencies import get_conversation_service
from app.modules.agent_surfaces.api.dependencies import (
    get_surface_service,
    surface_repository_factory,
)
from app.modules.agent_surfaces.domain.events import SurfaceWebhookReceivedEvent
from app.modules.agent_surfaces.domain.ingress_context import SurfaceChatContext
from app.modules.agent_surfaces.domain.ingress_request import (
    SurfaceDirectWebhookIngress,
    SurfacePlatformWebhookIngress,
    SurfaceScheduleIngress,
)
from app.modules.agent_surfaces.domain.job_payloads import (
    SurfaceProcessMessageTaskPayload,
)
from app.modules.agent_surfaces.infrastructure.adapters.routing_resolution_adapter import (
    SqlAlchemySurfaceRoutingResolutionAdapter,
)
from app.modules.agent_surfaces.infrastructure.repositories.surface_repository import (
    SurfaceConversationLinkRepository,
)
from app.modules.agent_surfaces.services.ingress_service import (
    AgentSurfaceIngressService,
)
from app.modules.connectors.api.dependencies import get_connector_service
from app.modules.pod.domain.events import PodDeletedEvent, PodEvents
from app.modules.schedule.domain.events.schedule import ScheduleEvents, ScheduleFired

logger = logging.getLogger(__name__)

router = RedisRouter()


async def provide_uow() -> AsyncGenerator[SqlAlchemyUnitOfWork, None]:
    async with create_uow_from_session_maker(async_session_maker) as uow:
        yield uow


def provide_surface_event_handler(
    uow: SqlAlchemyUnitOfWork = Depends(provide_uow),
) -> AgentSurfaceIngressService:
    return AgentSurfaceIngressService(
        uow=uow,
        surface_repository=surface_repository_factory(uow),
        conversation_link_repository=SurfaceConversationLinkRepository(uow),
        conversation_service=get_conversation_service(uow),
        connector_service=get_connector_service(uow),
        pod_membership_port=SqlAlchemySurfaceRoutingResolutionAdapter(uow),
    )


def provide_job_queue() -> SharedStreaqJobQueue:
    return get_streaq_job_queue()


@router.subscriber(stream=redis_stream_sub("surface_events"))
async def handle_surface_webhook(
    event: SurfaceWebhookReceivedEvent,
    fs_logger: Logger,
    uow: SqlAlchemyUnitOfWork = Depends(provide_uow),
    handler: AgentSurfaceIngressService = Depends(provide_surface_event_handler),
    job_queue: SharedStreaqJobQueue = Depends(provide_job_queue),
) -> None:
    try:
        fs_logger.info(f"Received webhook event for source: {event.source}")

        if event.surface_id:
            ingress_request = SurfaceDirectWebhookIngress(
                surface_id=event.surface_id,
                payload=event.payload,
                headers=event.headers or {},
            )
        else:
            ingress_request = SurfacePlatformWebhookIngress(
                source=event.source,
                payload=event.payload,
                headers=event.headers or {},
            )

        # Native-form submissions (Slack block_actions / Teams Action.Submit) are
        # routed back into their conversation as a new user message, not the
        # normal message ingress path.
        if await handler.try_handle_interaction(ingress_request):
            await uow.commit()
            fs_logger.info(
                "Handled surface interaction for webhook source=%s", event.source
            )
            return

        context = await handler.prepare_ingress(ingress_request)

        if not context:
            return

        if isinstance(context, SurfaceChatContext):
            await handler.start_agent_chat(context)
            # start_agent_chat commits the shared UoW internally; commit again
            # defensively so the conversation link persists even if that changes.
            await uow.commit()
            fs_logger.info("Started agent run for surface webhook source=%s", event.source)
            return

        await uow.commit()
        await job_queue.enqueue(
            "process_surface_message",
            payload=SurfaceProcessMessageTaskPayload(context=context).model_dump(
                mode="json"
            ),
        )
        fs_logger.info("Enqueued direct surface reply for webhook source=%s", event.source)
    except Exception as exc:
        fs_logger.error(f"Failed to process webhook event: {exc}", exc_info=True)


@router.subscriber(stream=redis_stream_sub(ScheduleEvents.STREAM))
async def handle_surface_schedule_event(
    event: ScheduleFired,
    fs_logger: Logger,
    uow: SqlAlchemyUnitOfWork = Depends(provide_uow),
    handler: AgentSurfaceIngressService = Depends(provide_surface_event_handler),
    job_queue: SharedStreaqJobQueue = Depends(provide_job_queue),
) -> None:
    try:
        context = await handler.prepare_ingress(
            SurfaceScheduleIngress(
                schedule_id=event.schedule_id,
                payload=event.payload,
                account_id=event.account_id,
                pod_id=event.pod_id,
                user_id=event.user_id,
            )
        )
        if not context:
            return
        if isinstance(context, SurfaceChatContext):
            await handler.start_agent_chat(context)
            await uow.commit()
            fs_logger.info(
                "Started agent run for surface schedule source=%s",
                event.schedule_id,
            )
            return

        await uow.commit()
        await job_queue.enqueue(
            "process_surface_message",
            payload=SurfaceProcessMessageTaskPayload(context=context).model_dump(
                mode="json"
            ),
        )
        fs_logger.info(
            "Enqueued process_surface_message for schedule source=%s",
            event.schedule_id,
        )
    except Exception as exc:
        fs_logger.error("Failed to process surface schedule event: %s", exc, exc_info=True)


@router.subscriber(stream=redis_stream_sub(PodEvents.STREAM))
async def on_pod_deleted(
    event: dict,
    fs_logger: Logger,
    uow: SqlAlchemyUnitOfWork = Depends(provide_uow),
) -> None:
    """Remove all surfaces for a deleted pod so its accounts become free."""
    if event.get("event_type") != PodDeletedEvent.get_event_type():
        return

    parsed = PodDeletedEvent.model_validate(event)
    fs_logger.info("Processing PodDeletedEvent for surface cleanup pod=%s", parsed.pod_id)

    count = await get_surface_service(uow).delete_all_surfaces_for_pod(parsed.pod_id)
    fs_logger.info("Removed %s surfaces for deleted pod %s", count, parsed.pod_id)


@streaq_task(name="process_surface_message")
async def process_surface_message(
    payload: dict,
):
    worker_ctx: AppWorkerContext = streaq_worker.context
    task_ctx = process_surface_message.context
    task_payload = SurfaceProcessMessageTaskPayload.model_validate(payload)
    logger.info(
        "Starting process_surface_message job %s for conversation %s",
        task_ctx.task_id,
        getattr(task_payload.context, "conversation_id", None),
    )
    async with worker_ctx.uow() as uow:
        service = worker_ctx.build_surface_event_handler(uow)
        await service.execute_chat(task_payload.context)
    logger.info(
        "Finished process_surface_message job %s for conversation %s",
        task_ctx.task_id,
        getattr(task_payload.context, "conversation_id", None),
    )
