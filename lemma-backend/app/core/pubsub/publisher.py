from faststream.redis import RedisBroker
from pydantic import BaseModel
from app.core.config import settings


class PubSubPublisher:
    """Publisher for pubsub."""

    def __init__(self):
        self.broker = RedisBroker(settings.redis_url)

    async def __aenter__(self):
        await self.broker.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.broker.stop()

    async def publish(self, stream: str, data: BaseModel):
        """Publish a message to a stream (for permanent events like triggers)."""
        await self.broker.publish(data, stream=stream)

    async def publish_channel(self, channel: str, data: BaseModel):
        """Publish a message to a channel (for realtime pubsub updates)."""
        await self.broker.publish(data, channel=channel)
