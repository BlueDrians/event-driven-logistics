-- KPI cards
SELECT
  COUNT(DISTINCT order_id) AS total_orders,
  COUNTIF(status = 'DELIVERED') AS delivered_orders,
  COUNTIF(status = 'DELAYED') AS delayed_orders,
  SAFE_DIVIDE(COUNTIF(NOT is_sla_breached), COUNT(*)) AS sla_achievement_rate
FROM `{{PROJECT_ID}}.logistics_analytics.logistics_events`
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY);

-- Top delay reasons
SELECT
  delay_reason,
  COUNT(*) AS total_events
FROM `{{PROJECT_ID}}.logistics_analytics.logistics_events`
WHERE delay_reason IS NOT NULL AND delay_reason != ''
GROUP BY delay_reason
ORDER BY total_events DESC;

-- Route performance ranking
SELECT *
FROM `{{PROJECT_ID}}.logistics_analytics.vw_route_performance`
ORDER BY sla_achievement_rate ASC, sla_breach_count DESC;
