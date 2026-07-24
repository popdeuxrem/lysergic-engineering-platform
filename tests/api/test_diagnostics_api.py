from runtime.api.diagnostics import DiagnosticsAPI
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceRegistry
from runtime.services.resolver import DependencyResolver


def _make_manager() -> ServiceManager:
    registry = ServiceRegistry()
    return ServiceManager(
        registry=registry,
        resolver=DependencyResolver(),
        lifecycle=LifecycleManager(),
        health=HealthService(),
        event_bus=EventBus(),
    )


def test_diagnostics_snapshot_empty() -> None:
    api = DiagnosticsAPI(_make_manager())
    snap = api.snapshot()
    assert snap["health"]["overall"] == "unknown"
    assert snap["services"]["count"] == 0
    assert snap["ready"] is False


def test_diagnostics_service_count() -> None:
    api = DiagnosticsAPI(_make_manager())
    assert api.service_count == 0


def test_diagnostics_list_service_ids_empty() -> None:
    api = DiagnosticsAPI(_make_manager())
    assert api.list_service_ids() == ()


def test_diagnostics_is_healthy_not_ready() -> None:
    api = DiagnosticsAPI(_make_manager())
    assert api.is_healthy() is False


def test_diagnostics_with_registered_services() -> None:
    manager = _make_manager()
    manager.registry.register(ServiceDefinition(service_id="svc-a"))
    manager.registry.register(ServiceDefinition(service_id="svc-b"))
    api = DiagnosticsAPI(manager)
    assert api.service_count == 2
    ids = api.list_service_ids()
    assert "svc-a" in ids
    assert "svc-b" in ids
