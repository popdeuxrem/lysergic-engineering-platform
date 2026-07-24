from __future__ import annotations

from typing import Any, Protocol

from runtime.api.assets import AssetsAPI
from runtime.api.diagnostics import DiagnosticsAPI
from runtime.api.extensions import ExtensionAPI
from runtime.api.knowledge import KnowledgeAPI
from runtime.api.projects import ProjectAPI
from runtime.api.runtime import RuntimeAPI
from runtime.api.validation import ValidationAPI
from runtime.api.workflows import WorkflowAPI
from runtime.services.manager import ServiceManager


class LEPService(Protocol):
    name: str
    version: str
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def ready(self) -> bool: ...


class LEP:
    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._runtime = RuntimeAPI(manager)
        self._extensions = ExtensionAPI(manager)
        self._projects = ProjectAPI(manager)
        self._assets = AssetsAPI(manager)
        self._knowledge = KnowledgeAPI(manager)
        self._workflows = WorkflowAPI(manager)
        self._validation = ValidationAPI(manager)
        self._diagnostics = DiagnosticsAPI(manager)

    @property
    def runtime(self) -> RuntimeAPI:
        return self._runtime

    @property
    def extensions(self) -> ExtensionAPI:
        return self._extensions

    @property
    def projects(self) -> ProjectAPI:
        return self._projects

    @property
    def assets(self) -> AssetsAPI:
        return self._assets

    @property
    def knowledge(self) -> KnowledgeAPI:
        return self._knowledge

    @property
    def workflows(self) -> WorkflowAPI:
        return self._workflows

    @property
    def validation(self) -> ValidationAPI:
        return self._validation

    @property
    def diagnostics(self) -> DiagnosticsAPI:
        return self._diagnostics

    @property
    def manager(self) -> ServiceManager:
        return self._manager

    def start(self) -> None:
        self._manager.initialize()

    def stop(self) -> None:
        self._manager.shutdown()

    @property
    def ready(self) -> bool:
        return self._manager.is_ready()

    def health(self) -> dict[str, Any]:
        report = self._manager.health_report()
        return {
            "status": report.overall.value,
            "ready": report.ready_count,
            "total": report.total_count,
            "services": {k: v.status.value for k, v in report.services.items()},
        }

    def version(self) -> dict[str, str]:
        return {"platform": "Lysergic Engineering Platform", "version": "0.1.0", "architecture": "LEP-ARCH-v0.1.0"}

    def summary(self) -> dict[str, Any]:
        return self._runtime.summary()


def create_lep(manager: ServiceManager) -> LEP:
    return LEP(manager)


def create_default_lep() -> LEP:
    from runtime.services.events import EventBus
    from runtime.services.health import HealthService
    from runtime.services.manager import ServiceManager
    from runtime.services.registry import ServiceRegistry
    from runtime.services.resolver import DependencyResolver
    registry = ServiceRegistry()
    resolver = DependencyResolver()
    health = HealthService()
    event_bus = EventBus()
    manager = ServiceManager(registry=registry, resolver=resolver, health=health, event_bus=event_bus)
    lep = LEP(manager)
    lep.start()
    return lep
