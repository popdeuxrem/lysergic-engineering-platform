from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


@dataclass
class ExtensionManifest:
    extension_id: str
    name: str
    version: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class ExtensionAPIProtocol(Protocol):
    def list(self) -> tuple[ExtensionManifest, ...]: ...

    def get(self, extension_id: str) -> ExtensionManifest | None: ...

    def register(self, manifest: ExtensionManifest) -> None: ...

    def unregister(self, extension_id: str) -> None: ...

    def count(self) -> int: ...


class ExtensionAPI:
    service_id = "api.extensions"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._extensions: dict[str, ExtensionManifest] = {}

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._extensions.clear()

    def list(self) -> tuple[ExtensionManifest, ...]:
        return tuple(self._extensions.values())

    def get(self, extension_id: str) -> ExtensionManifest | None:
        return self._extensions.get(extension_id)

    def register(self, manifest: ExtensionManifest) -> None:
        self._extensions[manifest.extension_id] = manifest

    def unregister(self, extension_id: str) -> None:
        self._extensions.pop(extension_id, None)

    def count(self) -> int:
        return len(self._extensions)


def create_extension_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(
        service_id="api.extensions",
        factory=lambda: ExtensionAPI(manager),
    )
