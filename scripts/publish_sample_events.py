"""Publish sample events to Pub/Sub.

Usage:
  export GCP_PROJECT_ID="id-project"
  export PUBSUB_TOPIC="logistics-events"
  python scripts/publish_sample_events.py
"""
import json
import os
from pathlib import Path
from google.cloud import pubsub_v1

PROJECT_ID = os.environ["GCP_PROJECT_ID"]
TOPIC = os.getenv("PUBSUB_TOPIC", "logistics-events")
INPUT = Path("data/sample/logistics_events_sample.jsonl")


def main():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC)
    count = 0
    for line in INPUT.read_text(encoding="utf-8").splitlines():
        payload = json.loads(line)
        publisher.publish(topic_path, json.dumps(payload).encode("utf-8")).result()
        count += 1
    print(f"Published {count} messages to {topic_path}")


if __name__ == "__main__":
    main()
