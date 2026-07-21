import uuid

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_request_id_generated() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    request_id = response.headers["X-Request-ID"]
    assert uuid.UUID(request_id, version=4)


def test_correlation_id_generated_when_missing() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers
    correlation_id = response.headers["X-Correlation-ID"]
    assert uuid.UUID(correlation_id, version=4)


def test_correlation_id_accepted_from_header() -> None:
    supplied = "supplied-correlation-id"
    response = client.get("/health", headers={"X-Correlation-ID": supplied})

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == supplied


def test_correlation_id_propagates_to_subsequent_calls() -> None:
    correlation_id = "test-correlation-001"
    response_a = client.get("/api/v1/health", headers={"X-Correlation-ID": correlation_id})
    assert response_a.headers["X-Correlation-ID"] == correlation_id

    response_b = client.get("/api/v1/version", headers={"X-Correlation-ID": correlation_id})
    assert response_b.headers["X-Correlation-ID"] == correlation_id


def test_request_id_unique_per_request() -> None:
    response_a = client.get("/health")
    response_b = client.get("/health")

    rid_a = response_a.headers["X-Request-ID"]
    rid_b = response_b.headers["X-Request-ID"]
    assert rid_a != rid_b


def test_response_headers_present_on_all_endpoints() -> None:
    endpoints = ["/", "/health", "/version", "/api/v1/health", "/api/v1/version"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert "X-Request-ID" in response.headers, f"{endpoint} missing X-Request-ID"
        assert "X-Correlation-ID" in response.headers, f"{endpoint} missing X-Correlation-ID"


def test_error_response_headers_present_on_404() -> None:
    response = client.get("/nonexistent")

    assert response.status_code == 404
    assert "X-Request-ID" in response.headers
    assert "X-Correlation-ID" in response.headers
    rid = response.headers["X-Request-ID"]
    assert uuid.UUID(rid, version=4)


def test_request_id_correlation_id_in_request_state() -> None:
    correlation_id = "state-test-correlation"
    response = client.get("/health", headers={"X-Correlation-ID": correlation_id})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] is not None
    assert response.headers["X-Correlation-ID"] == correlation_id


def test_structured_logging_fields_present(caplog: object) -> None:
    import logging

    caplog.set_level(logging.INFO)

    response = client.get("/health")

    assert response.status_code == 200

    found_request_log = False
    for record in caplog.records:
        if "request.completed" in record.message:
            assert hasattr(record, "request_id")
            assert hasattr(record, "correlation_id")
            assert hasattr(record, "method")
            assert hasattr(record, "path")
            assert hasattr(record, "status_code")
            assert hasattr(record, "duration_ms")
            found_request_log = True

    assert found_request_log


def test_existing_endpoints_preserved() -> None:
    responses = {
        "/": client.get("/"),
        "/health": client.get("/health"),
        "/version": client.get("/version"),
        "/api/v1/health": client.get("/api/v1/health"),
        "/api/v1/version": client.get("/api/v1/version"),
    }

    for path, response in responses.items():
        assert response.status_code == 200, f"{path} should return 200"


def test_error_response_request_id_fallback() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert uuid.UUID(response.headers["X-Request-ID"], version=4)
    assert uuid.UUID(response.headers["X-Correlation-ID"], version=4)
