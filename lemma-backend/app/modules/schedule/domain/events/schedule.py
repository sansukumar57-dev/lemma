from datetime import datetime
from uuid import UUID
from app.core.domain.events import DomainEvent
from app.modules.schedule.domain.schedule import ScheduleType


class ScheduleEvent(DomainEvent):
    schedule_id: UUID
    user_id: UUID
    schedule_type: ScheduleType


class ScheduleCreated(ScheduleEvent):
    event_type: str = "schedule.created"
    config: dict


class ScheduleUpdated(ScheduleEvent):
    event_type: str = "schedule.updated"
    config: dict


class ScheduleDeleted(ScheduleEvent):
    event_type: str = "schedule.deleted"


class ScheduleFired(ScheduleEvent):
    """Event emitted when any schedule source fires.

    Unified event for all schedule source types (TIME, WEBHOOK, DATASTORE).
    """

    event_type: str = "schedule.fired"
    payload: dict
    metadata: dict | None = None
    # Additional context for richer processing
    account_id: UUID | None = None  # For WEBHOOK schedules
    pod_id: UUID | None = None  # For pod-scoped table/file schedules
    scheduled_at: datetime | None = None  # For TIME schedules
    llm_output: dict | None = None  # For filtered events


class ScheduleEvents:
    STREAM = "schedule_events"
