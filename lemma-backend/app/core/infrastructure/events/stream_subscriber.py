from __future__ import annotations

from faststream.redis import StreamSub

from app.core.config import settings


def redis_stream_sub(
    stream: str,
    *,
    group: str | None = None,
    consumer: str | None = None,
) -> StreamSub:
    """Create a Redis Stream subscriber with a shared polling interval."""
    return StreamSub(
        stream,
        group=group,
        consumer=consumer,
        polling_interval=settings.redis_stream_polling_interval_ms,
    )
