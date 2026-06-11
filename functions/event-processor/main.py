import base64
import json
import logging
import os
from google.cloud import bigquery

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET", "logistics_analytics")
TABLE_ID = os.getenv("BQ_TABLE", "logistics_events")

client = bigquery.Client(project=PROJECT_ID) if PROJECT_ID else None


def process_logistics_event(event, context):
    """Pub/Sub-triggered function that writes logistics events to BigQuery"""
    if "data" not in event:
        logger.warning("No data field in Pub/Sub message")
        return

    payload = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

    row = {
        "event_id": payload.get("event_id"),
        "event_type": payload.get("event_type"),
        "order_id": payload.get("order_id"),
        "status": payload.get("status"),
        "branch": payload.get("branch"),
        "route": payload.get("route"),
        "driver_id": payload.get("driver_id"),
        "sla_minutes": payload.get("sla_minutes"),
        "actual_minutes": payload.get("actual_minutes"),
        "delay_reason": payload.get("delay_reason"),
        "is_sla_breached": payload.get("is_sla_breached"),
        "event_timestamp": payload.get("event_timestamp"),
        "ingested_at": context.timestamp if context else None,
    }

    if client is None:
        logger.info("local_processed_event", extra={"row": row})
        return

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    errors = client.insert_rows_json(table_ref, [row])
    if errors:
        logger.error("bigquery_insert_failed", extra={"errors": errors})
        raise RuntimeError(errors)
    logger.info("bigquery_insert_success", extra={"event_id": row["event_id"]})
