from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "service": "lep-control-plane",
        "status": "healthy",
        "version": "0.1.0",
    }

def test_version_endpoint() -> None:
    response = client.get("/version")

    assert response.status_code == 200

def test_version_endpoint_structure() -> None:
    response = client.get("/version")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "lep-control-plane"
    assert payload["version"] == "0.1.0"
    assert payload["environment"] == "development"

def test_versioned_health_endpoint() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200

def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "lep-control-plane"
    assert payload["message"] == "LEP Control Plane"
