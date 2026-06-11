CREATE SCHEMA IF NOT EXISTS `{{PROJECT_ID}}.logistics_analytics`
OPTIONS(location = "asia-southeast2");

CREATE TABLE IF NOT EXISTS `{{PROJECT_ID}}.logistics_analytics.logistics_events` (
  event_id STRING NOT NULL,
  event_type STRING,
  order_id STRING NOT NULL,
  status STRING,
  branch STRING,
  route STRING,
  driver_id STRING,
  sla_minutes INT64,
  actual_minutes INT64,
  delay_reason STRING,
  is_sla_breached BOOL,
  event_timestamp TIMESTAMP,
  ingested_at TIMESTAMP
)
PARTITION BY DATE(event_timestamp)
CLUSTER BY route, branch, status;
