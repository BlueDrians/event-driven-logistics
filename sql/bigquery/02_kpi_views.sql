CREATE OR REPLACE VIEW `{{PROJECT_ID}}.logistics_analytics.vw_daily_logistics_kpi` AS
SELECT
  DATE(event_timestamp) AS event_date,
  COUNT(DISTINCT order_id) AS total_orders,
  COUNTIF(status = 'DELIVERED') AS delivered_orders,
  COUNTIF(status = 'DELAYED') AS delayed_orders,
  COUNTIF(is_sla_breached) AS sla_breach_count,
  SAFE_DIVIDE(COUNTIF(NOT is_sla_breached), COUNT(*)) AS sla_achievement_rate,
  AVG(actual_minutes) AS avg_actual_minutes,
  AVG(sla_minutes) AS avg_sla_minutes
FROM `{{PROJECT_ID}}.logistics_analytics.logistics_events`
GROUP BY event_date;

CREATE OR REPLACE VIEW `{{PROJECT_ID}}.logistics_analytics.vw_route_performance` AS
SELECT
  route,
  branch,
  COUNT(DISTINCT order_id) AS total_orders,
  COUNTIF(status = 'DELIVERED') AS delivered_orders,
  COUNTIF(status = 'DELAYED') AS delayed_orders,
  COUNTIF(is_sla_breached) AS sla_breach_count,
  SAFE_DIVIDE(COUNTIF(NOT is_sla_breached), COUNT(*)) AS sla_achievement_rate,
  AVG(actual_minutes - sla_minutes) AS avg_variance_minutes
FROM `{{PROJECT_ID}}.logistics_analytics.logistics_events`
GROUP BY route, branch;
