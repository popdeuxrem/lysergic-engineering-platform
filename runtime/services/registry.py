from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class ServiceStatus(Enum):
    PENDING = "pending"
    INITIALIZING = "initializing"
    READY = "ready"
    FAILED = "failed"
    STOPPING = "stopping"
    STOPPED = "stopped"


class Service(Protocol):
    service_id: str
    dependencies: tuple[str, ...]

    def initialize(self) -> None: ...

    def shutdown(self) -> None: ...

    @property
    def status(self) -> ServiceStatus: ...


@dataclass
class ServiceDefinition:
    service_id: str
    dependencies: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    factory: Callable[[], Service] | None = None
    singleton: bool = True
    instance: Service | None = None


class ServiceRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, ServiceDefinition] = {}
        self._instances: dict[str, Service] = {}
        self._frozen = False

    def register(self, definition: ServiceDefinition) -> None:
        if self._frozen:
            raise RuntimeError("Service registry is frozen")
        if definition.service_id in self._definitions:
            raise ValueError(f"Service '{definition.service_id}' already registered")
        self._definitions[definition.service_id] = definition

    def register_instance(self, service: Service) -> None:
        if self._frozen:
            raise RuntimeError("Service registry is frozen")
        if service.service_id in self._instances:
            raise ValueError(f"Service instance '{service.service_id}' already registered")
        self._instances[service.service_id] = service

    def resolve(self, service_id: str) -> Service:
        if service_id in self._instances:
            return self._instances[service_id]
        if service_id in self._definitions:
            definition = self._definitions[service_id]
            if definition.factory and definition.singleton:
                instance = definition.factory()
                self._instances[service_id] = instance
                return instance
            if definition.instance is not None:
                return definition.instance
            raise RuntimeError(f"Service '{service_id}' has no instance and no factory")
        raise KeyError(f"Service '{service_id}' not found in registry")

    @property
    def definitions(self) -> dict[str, ServiceDefinition]:
        return dict(self._definitions)

    @property
    def instances(self) -> dict[str, Service]:
        return dict(self._instances)

    @property
    def frozen(self) -> bool:
        return self._frozen

    def freeze(self) -> None:
        self._frozen = True

    def __contains__(self, service_id: str) -> bool:
        return service_id in self._definitions or service_id in self._instances

    def __len__(self) -> int:
        return len(self._definitions) + len(self._instances)
