from fastapi.testclient import TestClient

from src.main import app
from src.api.v1.schemas.common import ErrorResponse
from src.api.v1.schemas.health import HealthResponse, VersionResponse

client = TestClient(app)


def test_health_endpoint_returns_typed_response() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    model = HealthResponse.model_validate(response.json())

    assert model.service == "lep-control-plane"
    assert model.status == "healthy"
    assert model.version == "0.1.0"


def test_version_endpoint_returns_typed_response() -> None:
    response = client.get("/api/v1/version")

    assert response.status_code == 200
    model = VersionResponse.model_validate(response.json())

    assert model.service == "lep-control-plane"
    assert model.version == "0.1.0"
    assert model.environment == "development"


def test_error_response_conforms_to_envelope() -> None:
    ErrorResponse.model_rebuild()
    ErrorResponse.model_validate(
        {
            "error": {
                "code": "TEST_ERROR",
                "message": "A test error occurred",
                "request_id": "abc-123",
            }
        }
    )


def test_openapi_schema_generated() -> None:
    schema = app.openapi()

    assert schema["openapi"] is not None
    assert "/api/v1/health" in schema["paths"]
    assert "/api/v1/version" in schema["paths"]

    health_path = schema["paths"]["/api/v1/health"]["get"]
    assert "responses" in health_path
    assert "200" in health_path["responses"]

    version_path = schema["paths"]["/api/v1/version"]["get"]
    assert "responses" in version_path
    assert "200" in version_path["responses"]


def test_v1_api_version_boundary_exists() -> None:
    response_health = client.get("/api/v1/health")
    response_version = client.get("/api/v1/version")

    assert response_health.status_code == 200
    assert response_version.status_code == 200


def test_root_endpoints_preserved() -> None:
    responses = {
        "/": client.get("/"),
        "/health": client.get("/health"),
        "/version": client.get("/version"),
    }

    for path, response in responses.items():
        assert response.status_code == 200, f"{path} should return 200"
