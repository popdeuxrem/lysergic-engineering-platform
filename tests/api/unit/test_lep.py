from typing import Any

from runtime.api import LEP
from runtime.services.registry import ServiceStatus


class CountingService:
    def __init__(self, sid: str = "core") -> None:
        self.service_id = sid
        self.dependencies: tuple[str, ...] = ()
        self._status = ServiceStatus.PENDING
    def initialize(self) -> None:
        self._status = ServiceStatus.READY
    def shutdown(self) -> None:
        self._status = ServiceStatus.STOPPED
    @property
    def status(self) -> ServiceStatus:
        return self._status


def _make_manager(with_service: bool = False) -> Any:
    from runtime.kernel.lifecycle import LifecycleManager
    from runtime.services.events import EventBus
    from runtime.services.health import HealthService
    from runtime.services.manager import ServiceManager
    from runtime.services.registry import ServiceDefinition, ServiceRegistry
    from runtime.services.resolver import DependencyResolver
    m = ServiceManager(registry=ServiceRegistry(), resolver=DependencyResolver(), lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus())
    if with_service:
        m.registry.register(ServiceDefinition(service_id="core", factory=lambda: CountingService()))
    return m


def test_facade_properties() -> None:
    lep = LEP(_make_manager())
    assert lep.runtime is not None
    assert lep.extensions is not None
    assert lep.projects is not None
    assert lep.assets is not None
    assert lep.knowledge is not None
    assert lep.workflows is not None
    assert lep.validation is not None
    assert lep.diagnostics is not None


def test_start_and_stop() -> None:
    lep = LEP(_make_manager(with_service=True))
    lep.start()
    assert lep.ready is True
    lep.stop()
    assert lep.ready is False


def test_health() -> None:
    lep = LEP(_make_manager())
    h = lep.health()
    assert "status" in h and "ready" in h and "total" in h


def test_health_after_start() -> None:
    lep = LEP(_make_manager(with_service=True))
    lep.start()
    h = lep.health()
    assert h["status"] == "ready"


def test_start_idempotent() -> None:
    lep = LEP(_make_manager(with_service=True))
    lep.start()
    lep.start()
    assert lep.ready is True


def test_version() -> None:
    lep = LEP(_make_manager())
    v = lep.version()
    assert v["platform"] == "Lysergic Engineering Platform"


def test_summary() -> None:
    lep = LEP(_make_manager())
    s = lep.summary()
    assert "platform" in s


def test_runtime_delegation() -> None:
    lep = LEP(_make_manager())
    assert lep.runtime.platform_name() == "Lysergic Engineering Platform"


def test_extensions_delegation() -> None:
    lep = LEP(_make_manager())
    lep.extensions.register("e1", "E1", "1.0.0")
    assert lep.extensions.count() == 1


def test_projects_delegation() -> None:
    lep = LEP(_make_manager())
    lep.projects.create("p1", "P1")
    assert lep.projects.count() == 1


def test_assets_delegation() -> None:
    lep = LEP(_make_manager())
    lep.assets.store("a1", "schema")
    assert lep.assets.count() == 1


def test_knowledge_delegation() -> None:
    lep = LEP(_make_manager())
    lep.knowledge.add("k1", "note", "Content")
    assert lep.knowledge.count() == 1


def test_workflows_delegation() -> None:
    lep = LEP(_make_manager())
    lep.workflows.create("wf1", "W")
    assert lep.workflows.count() == 1


def test_diagnostics_delegation() -> None:
    lep = LEP(_make_manager())
    s = lep.diagnostics.snapshot()
    assert "health" in s


def test_create_lep_factory() -> None:
    from runtime.api.lep import create_lep
    lep = create_lep(_make_manager())
    assert isinstance(lep, LEP)
