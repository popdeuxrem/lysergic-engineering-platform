from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


class ExtensionState(Enum):
    DISCOVERED = "discovered"
    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    REMOVED = "removed"


@dataclass
class ExtensionRecord:
    extension_id: str
    name: str
    version: str
    description: str = ""
    state: ExtensionState = ExtensionState.DISCOVERED
    source: str = ""
    installed_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ExtensionAPIProtocol(Protocol):
    def list(self) -> tuple[ExtensionRecord, ...]: ...
    def get(self, extension_id: str) -> ExtensionRecord | None: ...
    def register(self, extension_id: str, name: str, version: str, **kwargs: Any) -> ExtensionRecord: ...
    def install(self, extension_id: str, source: str) -> ExtensionRecord | None: ...
    def enable(self, extension_id: str) -> ExtensionRecord | None: ...
    def disable(self, extension_id: str) -> ExtensionRecord | None: ...
    def remove(self, extension_id: str) -> bool: ...
    def is_enabled(self, extension_id: str) -> bool: ...
    def count(self) -> int: ...
    def list_by_state(self, state: ExtensionState) -> tuple[ExtensionRecord, ...]: ...


class ExtensionAPI:
    service_id = "api.extensions"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._extensions: dict[str, ExtensionRecord] = {}

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._extensions.clear()

    def list(self) -> tuple[ExtensionRecord, ...]:
        return tuple(self._extensions.values())

    def get(self, extension_id: str) -> ExtensionRecord | None:
        return self._extensions.get(extension_id)

    def register(self, extension_id: str, name: str, version: str, **kwargs: Any) -> ExtensionRecord:
        record = ExtensionRecord(extension_id=extension_id, name=name, version=version, **kwargs)
        self._extensions[extension_id] = record
        return record

    def install(self, extension_id: str, source: str) -> ExtensionRecord | None:
        record = self._extensions.get(extension_id)
        if record is None:
            return None
        self._extensions[extension_id] = ExtensionRecord(
            extension_id=record.extension_id, name=record.name, version=record.version,
            description=record.description, state=ExtensionState.INSTALLED,
            source=source, installed_at=datetime.now(UTC), metadata=record.metadata,
        )
        return self._extensions[extension_id]

    def enable(self, extension_id: str) -> ExtensionRecord | None:
        record = self._extensions.get(extension_id)
        if record is None:
            return None
        self._extensions[extension_id] = ExtensionRecord(
            extension_id=record.extension_id, name=record.name, version=record.version,
            description=record.description, state=ExtensionState.ENABLED,
            source=record.source, installed_at=record.installed_at, metadata=record.metadata,
        )
        return self._extensions[extension_id]

    def disable(self, extension_id: str) -> ExtensionRecord | None:
        record = self._extensions.get(extension_id)
        if record is None:
            return None
        self._extensions[extension_id] = ExtensionRecord(
            extension_id=record.extension_id, name=record.name, version=record.version,
            description=record.description, state=ExtensionState.DISABLED,
            source=record.source, installed_at=record.installed_at, metadata=record.metadata,
        )
        return self._extensions[extension_id]

    def remove(self, extension_id: str) -> bool:
        if extension_id in self._extensions:
            del self._extensions[extension_id]
            return True
        return False

    def is_enabled(self, extension_id: str) -> bool:
        record = self._extensions.get(extension_id)
        return record is not None and record.state == ExtensionState.ENABLED

    def count(self) -> int:
        return len(self._extensions)

    def list_by_state(self, state: ExtensionState) -> tuple[ExtensionRecord, ...]:
        return tuple(r for r in self._extensions.values() if r.state == state)

    def metadata(self) -> dict[str, object]:
        return {"count": self.count(), "states": {s.value: len(self.list_by_state(s)) for s in ExtensionState}}


def create_extension_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(service_id="api.extensions", factory=lambda: ExtensionAPI(manager))
