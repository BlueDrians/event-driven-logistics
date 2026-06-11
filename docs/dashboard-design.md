# Dashboard Design

## KPI Cards

- Total Orders
- Delivered Orders
- Delayed Orders
- SLA Achievement Rate
- Average Delivery Time
- SLA Breach Count

## Charts

1. Daily order volume trend
2. SLA achievement by route
3. Delay reason breakdown
4. Top routes with SLA breach
5. Branch-level performance

## Filters

- Date range
- Branch
- Route
- Status
- Driver ID

## Recommended BigQuery Sources

- `vw_daily_logistics_kpi`
- `vw_route_performance`
- `logistics_events`
