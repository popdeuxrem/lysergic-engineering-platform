from runtime.api import LEP
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceRegistry, ServiceStatus
from runtime.services.resolver import DependencyResolver


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


def _make_manager(with_service: bool = False) -> ServiceManager:
    manager = ServiceManager(
        registry=ServiceRegistry(),
        resolver=DependencyResolver(),
        lifecycle=LifecycleManager(),
        health=HealthService(),
        event_bus=EventBus(),
    )
    if with_service:
        manager.registry.register(ServiceDefinition(
            service_id="core",
            factory=lambda: CountingService(),
        ))
    return manager


def test_lep_facade_properties() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    assert lep.runtime is not None
    assert lep.extensions is not None
    assert lep.projects is not None
    assert lep.assets is not None
    assert lep.knowledge is not None
    assert lep.workflows is not None
    assert lep.validation is not None
    assert lep.diagnostics is not None


def test_lep_start_and_stop() -> None:
    manager = _make_manager(with_service=True)
    lep = LEP(manager)
    lep.start()
    assert lep.ready is True
    lep.stop()
    assert lep.ready is False


def test_lep_health() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    health = lep.health()
    assert health["status"] == "unknown"
    assert health["ready"] == 0


def test_lep_health_after_start() -> None:
    manager = _make_manager(with_service=True)
    lep = LEP(manager)
    lep.start()
    health = lep.health()
    assert health["status"] == "ready"
    assert health["ready"] == 1


def test_lep_start_idempotent() -> None:
    manager = _make_manager(with_service=True)
    lep = LEP(manager)
    lep.start()
    lep.start()
    assert lep.ready is True


def test_lep_runtime_delegation() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    summary = lep.runtime.summary()
    assert summary["platform"] == "Lysergic Engineering Platform"


def test_lep_extensions_delegation() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    assert lep.extensions.count() == 0
    from runtime.api.extensions import ExtensionManifest
    lep.extensions.register(ExtensionManifest(extension_id="e1", name="E1", version="1.0.0"))
    assert lep.extensions.count() == 1


def test_lep_projects_delegation() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    lep.projects.create("p1", "Project 1")
    assert lep.projects.count() == 1


def test_lep_assets_delegation() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    lep.assets.store("a1", "schema")
    assert lep.assets.count() == 1


def test_lep_knowledge_delegation() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    lep.knowledge.add("k1", "note", "Content")
    assert lep.knowledge.count() == 1


def test_lep_workflows_delegation() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    lep.workflows.create("wf1", "Workflow 1")
    assert lep.workflows.count() == 1


def test_lep_diagnostics_delegation() -> None:
    manager = _make_manager()
    lep = LEP(manager)
    snap = lep.diagnostics.snapshot()
    assert "health" in snap
