provider "google" {
  project = "pubsub-425813"
  region = "us-central1"
}

resource "google_pubsub_topic" "sensor-data-topic" {
  name = "sensor-data-topic"
}

resource "google_pubsub_subscription" "sensor-data-subscription" {
  name  = "sensor-data-subscription"
  topic = google_pubsub_topic.sensor-data-topic.id

  ack_deadline_seconds = 20

  push_config {
    push_endpoint = "https://example.com/push"

    attributes = {
      x-goog-version = "v1"
    }
  }
}

resource "google_service_account" "pubsub" {
  account_id   = "pubsub-service-account"
  display_name = "Pub/Sub Service Account"
}

resource "google_service_account_iam_binding" "pubsub-invoker" {
  service_account_id = google_service_account.pubsub.name
  role               = "roles/iam.serviceAccountTokenCreator"
  members            = [
    "serviceAccount:${google_service_account.pubsub.email}"
  ]
}

output "service_account_email" {
  value = google_service_account.pubsub.email
}