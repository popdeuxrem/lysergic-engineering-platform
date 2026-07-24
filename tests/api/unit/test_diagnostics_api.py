from runtime.api.diagnostics import DiagnosticsAPI
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceRegistry
from runtime.services.resolver import DependencyResolver


def _make_manager() -> ServiceManager:
    return ServiceManager(
        registry=ServiceRegistry(), resolver=DependencyResolver(),
        lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus(),
    )


def test_snapshot_empty() -> None:
    api = DiagnosticsAPI(_make_manager())
    s = api.snapshot()
    assert s["health"]["overall"] == "unknown"
    assert s["services"]["count"] == 0


def test_snapshot_with_services() -> None:
    m = _make_manager()
    m.registry.register(ServiceDefinition(service_id="svc-a"))
    api = DiagnosticsAPI(m)
    s = api.snapshot()
    assert s["services"]["count"] == 1
    assert "svc-a" in s["services"]["registered"]


def test_record_error() -> None:
    api = DiagnosticsAPI(_make_manager())
    api.record_error("test", "error msg")
    s = api.snapshot()
    assert len(s["errors"]) == 1


def test_clear_errors() -> None:
    api = DiagnosticsAPI(_make_manager())
    api.record_error("test", "err")
    api.clear_errors()
    s = api.snapshot()
    assert len(s["errors"]) == 0


def test_telemetry_summary() -> None:
    api = DiagnosticsAPI(_make_manager())
    t = api.telemetry_summary()
    assert "event_count" in t
    assert "subscriber_count" in t


def test_service_count() -> None:
    api = DiagnosticsAPI(_make_manager())
    assert api.service_count == 0


def test_list_service_ids() -> None:
    api = DiagnosticsAPI(_make_manager())
    assert api.list_service_ids() == ()


def test_is_healthy() -> None:
    api = DiagnosticsAPI(_make_manager())
    assert api.is_healthy() is False
