# ADR 002: Use BigQuery for Logistics Analytics

## Status

Accepted

## Context

The dashboard requires aggregate queries by date, route, branch, driver, status, and delay reason

## Decision

Use BigQuery as the analytics warehouse for event data

## Consequences

### Positive

- Supports large-scale analytics without database management
- Integrates directly with Looker Studio
- Partitioning and clustering support cost optimization

### Trade-Offs

- Query design and partition filters are important for cost control
- Not intended for low-latency transactional reads
