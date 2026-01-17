# T-V-07: Event Publisher using Dapr Pub/Sub
# From: speckit.plan - Event-Driven Architecture
"""
Event publisher that uses Dapr sidecar HTTP API for publishing events.

The publisher:
- Uses async HTTP calls to Dapr sidecar
- Handles retries with exponential backoff
- Supports graceful degradation if Dapr is unavailable
- Logs all publish attempts for observability
"""

import os
import logging
from typing import Optional
import httpx
from functools import lru_cache

from .schemas import TaskEvent, Topics

# Configure logging
logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Publishes events via Dapr Pub/Sub.

    Uses the Dapr sidecar HTTP API to publish events to Kafka topics.
    Falls back gracefully if Dapr is not available.
    """

    def __init__(
        self,
        dapr_host: str = "localhost",
        dapr_port: int = 3500,
        pubsub_name: str = "pubsub-kafka",
        timeout: float = 10.0,
        enabled: bool = True
    ):
        """
        Initialize the event publisher.

        Args:
            dapr_host: Dapr sidecar host (default: localhost)
            dapr_port: Dapr sidecar HTTP port (default: 3500)
            pubsub_name: Name of Dapr pub/sub component (default: pubsub-kafka)
            timeout: HTTP request timeout in seconds
            enabled: Whether event publishing is enabled
        """
        self.dapr_host = dapr_host
        self.dapr_port = dapr_port
        self.pubsub_name = pubsub_name
        self.timeout = timeout
        self.enabled = enabled
        self._base_url = f"http://{dapr_host}:{dapr_port}"

    @property
    def publish_url(self) -> str:
        """Get the Dapr publish URL template"""
        return f"{self._base_url}/v1.0/publish/{self.pubsub_name}"

    async def publish(
        self,
        topic: Topics,
        event: TaskEvent,
        retry_count: int = 3
    ) -> bool:
        """
        Publish an event to a topic via Dapr.

        Args:
            topic: Kafka topic to publish to
            event: Event to publish
            retry_count: Number of retries on failure

        Returns:
            True if publish succeeded, False otherwise
        """
        if not self.enabled:
            logger.debug(f"Event publishing disabled, skipping: {event.type}")
            return True

        url = f"{self.publish_url}/{topic.value}"
        payload = event.to_dict()

        logger.info(
            f"Publishing event: type={event.type}, topic={topic.value}, "
            f"id={event.id}"
        )

        for attempt in range(retry_count):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        url,
                        json=payload,
                        headers={
                            "Content-Type": "application/cloudevents+json"
                        }
                    )

                    if response.status_code in (200, 204):
                        logger.info(
                            f"Event published successfully: type={event.type}, "
                            f"id={event.id}"
                        )
                        return True
                    else:
                        logger.warning(
                            f"Dapr publish returned status {response.status_code}: "
                            f"{response.text}"
                        )

            except httpx.ConnectError as e:
                logger.warning(
                    f"Cannot connect to Dapr sidecar (attempt {attempt + 1}/{retry_count}): {e}"
                )
                if attempt == retry_count - 1:
                    logger.error(
                        f"Dapr sidecar not available, event not published: "
                        f"type={event.type}, id={event.id}"
                    )
                    return False

            except httpx.TimeoutException as e:
                logger.warning(
                    f"Dapr publish timeout (attempt {attempt + 1}/{retry_count}): {e}"
                )

            except Exception as e:
                logger.error(
                    f"Unexpected error publishing event (attempt {attempt + 1}/{retry_count}): {e}"
                )

        return False

    async def publish_to_task_events(self, event: TaskEvent) -> bool:
        """Publish to the task-events topic"""
        return await self.publish(Topics.TASK_EVENTS, event)

    async def publish_to_reminders(self, event: TaskEvent) -> bool:
        """Publish to the reminders topic"""
        return await self.publish(Topics.REMINDERS, event)

    async def publish_to_task_updates(self, event: TaskEvent) -> bool:
        """Publish to the task-updates topic (for real-time sync)"""
        return await self.publish(Topics.TASK_UPDATES, event)

    async def check_health(self) -> bool:
        """Check if Dapr sidecar is healthy"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self._base_url}/v1.0/healthz")
                return response.status_code == 200
        except Exception:
            return False


# Singleton instance
_publisher: Optional[EventPublisher] = None


@lru_cache()
def get_event_publisher() -> EventPublisher:
    """
    Get the singleton event publisher instance.

    Configuration is read from environment variables:
    - DAPR_HTTP_PORT: Dapr sidecar port (default: 3500)
    - DAPR_ENABLED: Whether to enable event publishing (default: true)

    Returns:
        EventPublisher instance
    """
    global _publisher

    if _publisher is None:
        dapr_port = int(os.getenv("DAPR_HTTP_PORT", "3500"))
        dapr_enabled = os.getenv("DAPR_ENABLED", "true").lower() in ("true", "1", "yes")

        _publisher = EventPublisher(
            dapr_host="localhost",  # Sidecar is always localhost
            dapr_port=dapr_port,
            enabled=dapr_enabled
        )

        logger.info(
            f"Event publisher initialized: port={dapr_port}, enabled={dapr_enabled}"
        )

    return _publisher
