# Operations Runbook

## Common Incidents

### API 5xx Error Spike

1. Check Cloud Run revision logs
2. Validate recent deployment status
3. Check Pub/Sub publish permissions
4. Roll back to previous revision if needed

### Pub/Sub Backlog Increasing

1. Check event processor logs
2. Validate BigQuery insert errors
3. Inspect schema mismatch or invalid payloads
4. Route failed messages to dead-letter topic

### Dashboard Data Delayed

1. Check BigQuery table ingestion time
2. Validate Looker Studio data freshness
3. Check query filters and partition range

## SLO Examples

| Service | SLO |
|---|---:|
| Order API availability | 99.5% |
| Event processing latency | < 5 minutes p95 |
| Dashboard freshness | < 15 minutes |
