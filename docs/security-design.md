# Security Design

## Identity and Access

| Workload | Service Account | Minimum Role |
|---|---|---|
| Cloud Run Order API | `sa-logistics-order-api` | Pub/Sub Publisher |
| Event Processor | `sa-logistics-processor` | BigQuery Data Editor |
| CI/CD | Cloud Build SA | Cloud Run Developer, Artifact Registry Writer |

## Security Controls

- Use dedicated service accounts per workload
- Avoid service account keys. Prefer Workload Identity Federation or Cloud Build identity
- Keep Cloud Run private by default and expose through API Gateway
- Apply least privilege IAM roles
- Store runtime secrets in Secret Manager if database or third-party API integration is added
- Do not store raw customer data in GitHub
- Partition customer data and apply access controls at dataset level

## Data Protection

The sample dataset is dummy data only. In production, customer identifiers should be tokenized or minimized where possible
