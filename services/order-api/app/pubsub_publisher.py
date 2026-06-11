import json
import logging
from google.cloud import pubsub_v1
from .config import settings
from .models import LogisticsEvent

logger = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self) -> None:
        self._client = None
        if settings.publish_events:
            self._client = pubsub_v1.PublisherClient()

    def publish(self, event: LogisticsEvent) -> str:
        payload = event.model_dump(mode="json")
        payload["is_sla_breached"] = event.is_sla_breached

        if not settings.publish_events:
            logger.info("local_event_generated", extra={"event": payload})
            return "local-log-only"

        topic_path = self._client.topic_path(settings.gcp_project_id, settings.pubsub_topic)
        future = self._client.publish(topic_path, json.dumps(payload).encode("utf-8"))
        message_id = future.result(timeout=10)
        logger.info("event_published", extra={"message_id": message_id, "order_id": event.order_id})
        return message_id


publisher = EventPublisher()
