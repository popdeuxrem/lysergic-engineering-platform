from runtime.api.runtime import RuntimeAPI
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceRegistry
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


def test_runtime_api_platform_name() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.platform_name() == "Lysergic Engineering Platform"


def test_runtime_api_platform_version() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.platform_version() == "0.1.0"


def test_runtime_api_architecture_id() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.architecture_id() == "LEP-ARCH-v0.1.0"


def test_runtime_api_architecture_status() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.architecture_status() == "frozen"


def test_runtime_api_schema_dialect() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.schema_dialect() == "draft2020-12"


def test_runtime_api_service_ids() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.service_ids() == ()


def test_runtime_api_service_count() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.service_count() == 0


def test_runtime_api_is_governance_enabled() -> None:
    api = RuntimeAPI(_make_manager())
    assert api.is_governance_enabled() is True


def test_runtime_api_summary() -> None:
    api = RuntimeAPI(_make_manager())
    summary = api.summary()
    assert summary["platform"] == "Lysergic Engineering Platform"
    assert summary["version"] == "0.1.0"
    assert summary["architecture"] == "LEP-ARCH-v0.1.0"
    assert summary["schema_dialect"] == "draft2020-12"
    assert summary["governance"] is True
