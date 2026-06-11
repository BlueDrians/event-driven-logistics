from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import uuid4


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELAYED = "DELAYED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class StatusUpdateRequest(BaseModel):
    status: OrderStatus
    branch: str = Field(..., examples=["Jakarta Hub"])
    route: str = Field(..., examples=["JKT-BDG"])
    driver_id: str = Field(..., examples=["DRV-001"])
    sla_minutes: int = Field(..., ge=1, examples=[1440])
    actual_minutes: int = Field(..., ge=0, examples=[1325])
    delay_reason: str | None = Field(default=None, examples=["Traffic congestion"])


class LogisticsEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt-{uuid4()}")
    event_type: str = "ORDER_STATUS_UPDATED"
    order_id: str
    status: OrderStatus
    branch: str
    route: str
    driver_id: str
    sla_minutes: int
    actual_minutes: int
    delay_reason: str | None = None
    event_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_sla_breached(self) -> bool:
        return self.actual_minutes > self.sla_minutes
