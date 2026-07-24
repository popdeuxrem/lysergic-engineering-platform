from runtime.api.runtime import RuntimeAPI
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceRegistry
from runtime.services.resolver import DependencyResolver


def _make_manager() -> ServiceManager:
    return ServiceManager(
        registry=ServiceRegistry(), resolver=DependencyResolver(),
        lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus(),
    )


def test_platform_name() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.platform_name() == "Lysergic Engineering Platform"


def test_platform_version() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.platform_version() == "0.1.0"


def test_architecture_id() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.architecture_id() == "LEP-ARCH-v0.1.0"


def test_architecture_status() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.architecture_status() == "frozen"


def test_schema_dialect() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.schema_dialect() == "draft2020-12"


def test_service_ids_empty() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.service_ids() == ()


def test_service_count() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.service_count() == 0


def test_is_governance_enabled() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.is_governance_enabled() is True


def test_runtime_status() -> None:
    api = RuntimeAPI(_make_manager())
    status = api.runtime_status()
    assert "ready" in status
    assert "health" in status
    assert "lifecycle" in status


def test_uptime_not_started() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.uptime() == "not started"


def test_summary() -> None:
    api = RuntimeAPI(_make_manager())
    s = api.summary()
    assert s["platform"] == "Lysergic Engineering Platform"
    assert s["version"] == "0.1.0"
    assert s["architecture"] == "LEP-ARCH-v0.1.0"
