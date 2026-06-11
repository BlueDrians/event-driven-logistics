# Event Schema

| Field | Type | Description |
|---|---|---|
| event_id | string | Unique event identifier |
| event_type | string | Event name, e.g. `ORDER_STATUS_UPDATED` |
| order_id | string | Order identifier |
| status | string | Current order status |
| branch | string | Branch or hub |
| route | string | Delivery route code |
| driver_id | string | Driver identifier |
| sla_minutes | integer | Expected SLA duration |
| actual_minutes | integer | Actual duration |
| delay_reason | string | Delay category if any |
| is_sla_breached | boolean | True when actual duration exceeds SLA |
| event_timestamp | timestamp | Event creation timestamp |
