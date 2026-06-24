"""Background jobs for schedule processing.

Note: workflow module owns consumption of ``schedule_events`` stream for starting/resuming
workflow runs. Keeping an additional no-op subscriber here can cause nondeterministic
message consumption.
"""

from typing import Any
from faststream.redis import RedisRouter

from app.core.infrastructure.jobs.streaq_runtime import AppWorkerContext, streaq_task, streaq_worker
from app.modules.schedule.repositories.schedule_repository import ScheduleRepository
from app.modules.schedule.services.schedule_filter_job_service import ScheduleFilterJobService
from app.core.log.log import get_logger

router = RedisRouter()
logger = get_logger(__name__)


@streaq_task(name="handle_llm_filter_task")
async def handle_llm_filter_task(
    payload: dict[str, Any],
    metadata: dict[str, Any],
    schedule_id: str | None = None,
) -> None:
    """Apply LLM filtering to a webhook event."""
    worker_ctx: AppWorkerContext = streaq_worker.context
    if schedule_id is None:
        raise ValueError("schedule_id is required")
    logger.info(f"Processing LLM filtering for schedule {schedule_id}")

    async with worker_ctx.uow() as uow:
        service = ScheduleFilterJobService(ScheduleRepository(uow=uow))
        await service.process(
            schedule_id=schedule_id,
            payload=payload,
            metadata=metadata,
        )
