from __future__ import annotations

from typing import AsyncGenerator

from faststream import Depends, Logger
from faststream.redis import RedisRouter

from app.core.infrastructure.db.uow_factory import create_uow_from_session_maker
from app.core.infrastructure.events.message_bus import get_message_bus
from app.core.infrastructure.events.stream_subscriber import redis_stream_sub
from app.modules.datastore.domain.events import (
    DATASTORE_EVENTS_STREAM,
    DatastoreRecordEvent,
)
from app.modules.schedule.repositories.schedule_repository import ScheduleRepository
from app.modules.schedule.services.datastore_event_handler import DatastoreEventHandler
from app.modules.schedule.services.schedule_processor import ScheduleProcessor
from app.core.infrastructure.db.session import async_session_maker
from app.core.infrastructure.db.uow import SqlAlchemyUnitOfWork
from app.core.log.log import get_logger

router = RedisRouter()
logger = get_logger(__name__)


async def provide_uow() -> AsyncGenerator[SqlAlchemyUnitOfWork, None]:
    """Provide UoW for schedule datastore event handlers."""
    async with create_uow_from_session_maker(async_session_maker) as uow:
        yield uow


def provide_datastore_event_handler(
    uow: SqlAlchemyUnitOfWork = Depends(provide_uow),
) -> DatastoreEventHandler:
    message_bus = get_message_bus()
    return DatastoreEventHandler(
        schedule_repository=ScheduleRepository(uow=uow, message_bus=message_bus),
        schedule_processor=ScheduleProcessor(),
    )


@router.subscriber(stream=redis_stream_sub(DATASTORE_EVENTS_STREAM))
async def handle_datastore_event(
    event: dict,
    fs_logger: Logger,
    handler: DatastoreEventHandler = Depends(provide_datastore_event_handler),
):
    """Handle datastore record events and fire matching schedules.

    The unified datastore stream also carries datastore/table/file events; only
    record events (``datastore.record.*``) drive schedules, so anything else is
    ignored here.
    """
    event_type = event.get("event_type", "")
    if not event_type.startswith("datastore.record."):
        return

    record_event = DatastoreRecordEvent.model_validate(event)
    fs_logger.info(
        f"Received DatastoreRecordEvent: {record_event.operation.value} "
        f"on {record_event.table_name}"
    )

    schedule_ids = await handler.handle_datastore_event(record_event)
    if schedule_ids:
        fs_logger.info(f"Fired {len(schedule_ids)} DATASTORE schedules")
