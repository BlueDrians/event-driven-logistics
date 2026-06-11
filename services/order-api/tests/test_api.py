from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_update_order_status():
    payload = {
        "status": "IN_TRANSIT",
        "branch": "Jakarta Hub",
        "route": "JKT-BDG",
        "driver_id": "DRV-001",
        "sla_minutes": 1440,
        "actual_minutes": 1325,
    }
    response = client.post("/orders/ORD-2026-0001/status", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["order_id"] == "ORD-2026-0001"
    assert body["is_sla_breached"] is False
