from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


@dataclass
class ProjectManifest:
    project_id: str
    name: str
    version: str = "0.1.0"
    description: str = ""
    workspace: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ProjectAPIProtocol(Protocol):
    def create(self, project_id: str, name: str, **kwargs: Any) -> ProjectManifest: ...
    def get(self, project_id: str) -> ProjectManifest | None: ...
    def list(self) -> tuple[ProjectManifest, ...]: ...
    def search(self, query: str) -> tuple[ProjectManifest, ...]: ...
    def update(self, project_id: str, **kwargs: Any) -> ProjectManifest | None: ...
    def remove(self, project_id: str) -> bool: ...
    def count(self) -> int: ...


class ProjectAPI:
    service_id = "api.projects"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._projects: dict[str, ProjectManifest] = {}

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._projects.clear()

    def create(self, project_id: str, name: str, **kwargs: Any) -> ProjectManifest:
        manifest = ProjectManifest(project_id=project_id, name=name, **kwargs)
        self._projects[project_id] = manifest
        return manifest

    def get(self, project_id: str) -> ProjectManifest | None:
        return self._projects.get(project_id)

    def list(self) -> tuple[ProjectManifest, ...]:
        return tuple(self._projects.values())

    def search(self, query: str) -> tuple[ProjectManifest, ...]:
        q = query.lower()
        return tuple(
            p for p in self._projects.values()
            if q in p.name.lower() or q in p.project_id.lower() or q in p.description.lower()
        )

    def update(self, project_id: str, **kwargs: Any) -> ProjectManifest | None:
        current = self._projects.get(project_id)
        if current is None:
            return None
        manifest = ProjectManifest(
            project_id=current.project_id, name=kwargs.get("name", current.name),
            version=kwargs.get("version", current.version),
            description=kwargs.get("description", current.description),
            workspace=kwargs.get("workspace", current.workspace),
            created_at=current.created_at, updated_at=datetime.now(UTC),
            metadata=kwargs.get("metadata", current.metadata),
        )
        self._projects[project_id] = manifest
        return manifest

    def remove(self, project_id: str) -> bool:
        if project_id in self._projects:
            del self._projects[project_id]
            return True
        return False

    def count(self) -> int:
        return len(self._projects)


def create_project_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(service_id="api.projects", factory=lambda: ProjectAPI(manager))
