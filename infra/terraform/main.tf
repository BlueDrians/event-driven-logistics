resource "google_project_service" "services" {
  for_each = toset([
    "run.googleapis.com",
    "cloudfunctions.googleapis.com",
    "eventarc.googleapis.com",
    "pubsub.googleapis.com",
    "bigquery.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "apigateway.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com"
  ])

  project = var.project_id
  service = each.key

  disable_on_destroy = false
}

resource "google_pubsub_topic" "logistics_events" {
  name = "logistics-events-${var.environment}"

  message_retention_duration = "604800s"

  labels = {
    environment = var.environment
    workload    = "logistics"
  }

  depends_on = [google_project_service.services]
}

resource "google_pubsub_topic" "dead_letter" {
  name = "logistics-events-dlq-${var.environment}"

  labels = {
    environment = var.environment
    workload    = "logistics"
  }

  depends_on = [google_project_service.services]
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id                 = "logistics_analytics_${var.environment}"
  location                   = "asia-southeast2"
  delete_contents_on_destroy = true

  labels = {
    environment = var.environment
    workload    = "logistics"
  }
}

resource "google_bigquery_table" "events" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  table_id   = "logistics_events"

  deletion_protection = false

  time_partitioning {
    type  = "DAY"
    field = "event_timestamp"
  }

  clustering = ["route", "branch", "status"]

  schema = jsonencode([
    { name = "event_id", type = "STRING", mode = "REQUIRED" },
    { name = "event_type", type = "STRING", mode = "NULLABLE" },
    { name = "order_id", type = "STRING", mode = "REQUIRED" },
    { name = "status", type = "STRING", mode = "NULLABLE" },
    { name = "branch", type = "STRING", mode = "NULLABLE" },
    { name = "route", type = "STRING", mode = "NULLABLE" },
    { name = "driver_id", type = "STRING", mode = "NULLABLE" },
    { name = "sla_minutes", type = "INTEGER", mode = "NULLABLE" },
    { name = "actual_minutes", type = "INTEGER", mode = "NULLABLE" },
    { name = "delay_reason", type = "STRING", mode = "NULLABLE" },
    { name = "is_sla_breached", type = "BOOLEAN", mode = "NULLABLE" },
    { name = "event_timestamp", type = "TIMESTAMP", mode = "NULLABLE" },
    { name = "ingested_at", type = "TIMESTAMP", mode = "NULLABLE" }
  ])
}

resource "google_service_account" "order_api" {
  account_id   = "sa-logistics-order-api-${var.environment}"
  display_name = "Logistics Order API Service Account"
}

resource "google_service_account" "event_processor" {
  account_id   = "sa-logistics-processor-${var.environment}"
  display_name = "Logistics Event Processor Service Account"
}

resource "google_pubsub_topic_iam_member" "publisher" {
  topic  = google_pubsub_topic.logistics_events.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.order_api.email}"
}

resource "google_bigquery_dataset_iam_member" "processor_editor" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${google_service_account.event_processor.email}"
}

# Cloud Run service is represented as a placeholder because image build/push varies by project.
# In production, connect this to Artifact Registry and Cloud Build.
resource "google_cloud_run_v2_service" "order_api" {
  name     = "logistics-order-api-${var.environment}"
  location = var.region

  template {
    service_account = google_service_account.order_api.email

    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "PUBSUB_TOPIC"
        value = google_pubsub_topic.logistics_events.name
      }

      env {
        name  = "PUBLISH_EVENTS"
        value = "true"
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }
  }

  depends_on = [google_project_service.services]
}

resource "google_monitoring_alert_policy" "cloud_run_5xx" {
  display_name = "Logistics API - High 5xx Error Rate"
  combiner     = "OR"

  conditions {
    display_name = "Cloud Run 5xx errors"

    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_count\" AND metric.labels.response_code_class=\"5xx\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 5

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  enabled = true
}
