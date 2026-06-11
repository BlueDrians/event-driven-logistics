# ADR 001: Use Event-Driven Architecture for Logistics Status Updates

## Status

Accepted

## Context

Order status updates arrive from different systems and users. The platform needs to accept updates quickly while allowing analytics processing to happen independently

## Decision

Use Pub/Sub as the central event bus between the Cloud Run API and downstream processors

## Consequences

### Positive

- API remains responsive even if analytics processing is delayed
- Multiple consumers can be added later
- Event replay and dead-letter handling can improve resilience

### Trade-Offs

- Requires event schema governance
- Requires monitoring for message backlog and failed processing
