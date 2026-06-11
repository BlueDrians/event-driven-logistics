import logging
from fastapi import FastAPI
from .config import settings
from .models import LogisticsEvent, StatusUpdateRequest
from .pubsub_publisher import publisher

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

app = FastAPI(
    title="Event-Driven Logistics Order API",
    description="Sample Cloud Run API for publishing logistics order events to Pub/Sub",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }


@app.post("/orders/{order_id}/status")
def update_order_status(order_id: str, request: StatusUpdateRequest) -> dict:
    event = LogisticsEvent(order_id=order_id, **request.model_dump())
    message_id = publisher.publish(event)
    return {
        "message": "Order status event accepted",
        "order_id": order_id,
        "event_id": event.event_id,
        "status": event.status,
        "is_sla_breached": event.is_sla_breached,
        "pubsub_message_id": message_id,
    }
