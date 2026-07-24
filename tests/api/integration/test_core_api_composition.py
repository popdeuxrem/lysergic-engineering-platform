"""Integration tests for Core API domain composition."""

from runtime.api import LEP
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceRegistry, ServiceStatus
from runtime.services.resolver import DependencyResolver


class CountingService:
    def __init__(self, sid: str = "svc") -> None:
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


def _make_lep() -> LEP:
    m = ServiceManager(registry=ServiceRegistry(), resolver=DependencyResolver(), lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus())
    return LEP(m)


def test_full_workflow_lifecycle() -> None:
    lep = _make_lep()
    wf = lep.workflows.create("wf-1", "Integration Test", steps=("validate", "deploy"))
    assert wf.status.name == "PENDING"

    started = lep.workflows.start("wf-1")
    assert started is not None and started.status.name == "RUNNING"

    completed = lep.workflows.complete("wf-1")
    assert completed is not None and completed.status.name == "COMPLETED"

    assert len(lep.workflows.history()) == 1


def test_extension_full_lifecycle() -> None:
    lep = _make_lep()
    lep.extensions.register("ext-1", "Full Cycle", "1.0.0")
    lep.extensions.install("ext-1", "/tmp/ext-1")
    lep.extensions.enable("ext-1")
    assert lep.extensions.is_enabled("ext-1") is True
    lep.extensions.disable("ext-1")
    assert lep.extensions.is_enabled("ext-1") is False


def test_project_search_and_update() -> None:
    lep = _make_lep()
    lep.projects.create("proj-1", "Core", description="Core system")
    lep.projects.create("proj-2", "Extensions", description="Plugin system")

    assert len(lep.projects.search("core")) == 1
    assert len(lep.projects.search("plugin")) == 1

    lep.projects.update("proj-1", name="Core v2")
    p = lep.projects.get("proj-1")
    assert p is not None and p.name == "Core v2"


def test_asset_discovery() -> None:
    lep = _make_lep()
    lep.assets.store("schema-1", "schema", tags=("draft", "core"))
    lep.assets.store("contract-1", "contract", tags=("v1",))
    lep.assets.store("template-1", "template")

    assert len(lep.assets.list_by_type("schema")) == 1
    assert "schema" in lep.assets.list_types()
    assert len(lep.assets.search("draft")) == 1


def test_knowledge_with_sources() -> None:
    lep = _make_lep()
    lep.knowledge.register_source("docs", "Documentation", kind="guide")
    lep.knowledge.register_source("api-ref", "API Reference", kind="reference")

    lep.knowledge.add("entry-1", "guide", "Getting started", source="docs")
    lep.knowledge.add("entry-2", "reference", "API v1", source="api-ref")

    lep.knowledge.index("entry-1")
    entry = lep.knowledge.get("entry-1")
    assert entry is not None and entry.indexed_at is not None

    assert len(lep.knowledge.sources()) == 2


def test_diagnostics_snapshot() -> None:
    lep = _make_lep()
    snap = lep.diagnostics.snapshot()
    assert "health" in snap
    assert "services" in snap
    assert "lifecycle" in snap

    telemetry = lep.diagnostics.telemetry_summary()
    assert "event_count" in telemetry
