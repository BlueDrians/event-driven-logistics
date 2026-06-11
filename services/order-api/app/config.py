import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "logistics-order-api")
    environment: str = os.getenv("ENVIRONMENT", "local")
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "local-project")
    pubsub_topic: str = os.getenv("PUBSUB_TOPIC", "logistics-events")
    publish_events: bool = os.getenv("PUBLISH_EVENTS", "false").lower() == "true"


settings = Settings()
