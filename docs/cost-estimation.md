# Cost Estimation

## Assumptions

| Component | Assumption |
|---|---:|
| API requests | 100,000 requests/month |
| Pub/Sub messages | 100,000 messages/month |
| BigQuery storage | 5 GB active storage |
| BigQuery queries | 100 GB processed/month |
| Cloud Run min instances | 0 for dev/test |
| Region | asia-southeast2 |

## Cost Drivers

1. Cloud Run request volume, CPU, and memory allocation
2. Pub/Sub message throughput and retention
3. Cloud Function invocation and runtime duration
4. BigQuery storage and query bytes processed
5. Logging volume and retention

## Optimization Recommendations

- Use Cloud Run min instances only for production workloads that require low latency
- Partition BigQuery tables by event date
- Cluster BigQuery tables by route, branch, and status
- Build Looker Studio dashboards on curated views instead of raw tables
- Add budget alerts per environment
- Apply retention policy for low-value logs

## Presales Note

For a customer proposal, present this as a variable-cost architecture. The platform starts with a low baseline cost and scales with actual operational volume
