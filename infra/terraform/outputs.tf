output "pubsub_topic" {
  value = google_pubsub_topic.logistics_events.name
}

output "bigquery_dataset" {
  value = google_bigquery_dataset.analytics.dataset_id
}

output "cloud_run_service" {
  value = google_cloud_run_v2_service.order_api.name
}
