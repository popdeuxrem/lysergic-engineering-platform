from __future__ import annotations

from typing import Any, Protocol

from runtime.api.assets import AssetRecord as AssetRecord
from runtime.api.assets import AssetsAPI as AssetsAPI
from runtime.api.diagnostics import DiagnosticsAPI as DiagnosticsAPI
from runtime.api.extensions import ExtensionAPI as ExtensionAPI
from runtime.api.knowledge import KnowledgeAPI as KnowledgeAPI
from runtime.api.projects import ProjectAPI as ProjectAPI
from runtime.api.runtime import RuntimeAPI as RuntimeAPI
from runtime.api.validation import ValidationAPI as ValidationAPI
from runtime.api.workflows import WorkflowAPI as WorkflowAPI
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
