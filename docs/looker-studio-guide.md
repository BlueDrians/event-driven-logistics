# Looker Studio Guide

## Data Source

Connect Looker Studio to BigQuery and use the curated views from `sql/bigquery/02_kpi_views.sql`

## Suggested Pages

1. Executive Overview
2. SLA and Delay Analysis
3. Route Performance
4. Branch Performance
5. Operational Drilldown

## Suggested Controls

- Date range control
- Branch filter
- Route filter
- Status filter

## Chart Mapping

| Dashboard Element | BigQuery Source |
|---|---|
| KPI Cards | `vw_daily_logistics_kpi` |
| SLA Trend | `vw_daily_logistics_kpi` |
| Route Ranking | `vw_route_performance` |
| Delay Reason Breakdown | `logistics_events` |
