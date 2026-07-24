from runtime.services.diagnostics import Diagnostics
from runtime.services.health import HealthService
from runtime.services.registry import ServiceDefinition, ServiceRegistry


def test_snapshot_with_empty_state() -> None:
    registry = ServiceRegistry()
    health = HealthService()
    diag = Diagnostics(registry, health)
    snap = diag.snapshot()
    assert snap.registry_size == 0
    assert snap.registered_ids == ()
    assert snap.instance_ids == ()
    assert snap.health is not None


def test_snapshot_with_registered_services() -> None:
    registry = ServiceRegistry()
    registry.register(ServiceDefinition(service_id="svc-a"))
    registry.register(ServiceDefinition(service_id="svc-b"))
    health = HealthService()
    diag = Diagnostics(registry, health)
    snap = diag.snapshot()
    assert snap.registry_size == 2
    assert "svc-a" in snap.registered_ids
    assert "svc-b" in snap.registered_ids


def test_record_error() -> None:
    registry = ServiceRegistry()
    health = HealthService()
    diag = Diagnostics(registry, health)
    diag.record_error("test", "something went wrong")
    snap = diag.snapshot()
    assert len(snap.errors) == 1
    assert snap.errors[0]["source"] == "test"
    assert snap.errors[0]["message"] == "something went wrong"


def test_clear_errors() -> None:
    registry = ServiceRegistry()
    health = HealthService()
    diag = Diagnostics(registry, health)
    diag.record_error("test", "error")
    diag.clear_errors()
    snap = diag.snapshot()
    assert len(snap.errors) == 0


def test_snapshot_to_dict() -> None:
    registry = ServiceRegistry()
    health = HealthService()
    diag = Diagnostics(registry, health)
    d = diag.snapshot().to_dict()
    assert "timestamp" in d
    assert "registry_size" in d
    assert "health" in d
