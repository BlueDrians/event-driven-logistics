# Deployment Guide

## Prerequisites

- Google Cloud project
- Billing enabled
- Terraform CLI
- gcloud CLI
- Docker
- Required IAM permissions to create Cloud Run, Pub/Sub, BigQuery, and IAM resources

## 1. Configure Terraform

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit:

```hcl
project_id  = "gcp-project-id"
region      = "asia-southeast2"
environment = "dev"
```

## 2. Deploy Infrastructure

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

## 3. Build and Deploy Cloud Run API

```bash
gcloud builds submit --config deploy/cloudbuild.yaml .
```

## 4. Create BigQuery Views

Replace `{{PROJECT_ID}}` in SQL files, then run:

```bash
bq query --use_legacy_sql=false < sql/bigquery/01_create_tables.sql
bq query --use_legacy_sql=false < sql/bigquery/02_kpi_views.sql
```

## 5. Connect Looker Studio

Use BigQuery connector and select the curated views:

- `vw_daily_logistics_kpi`
- `vw_route_performance`

## 6. Validate

- Check Cloud Run `/health` endpoint
- Publish sample order event
- Confirm rows in BigQuery
- Open dashboard and verify KPI cards
