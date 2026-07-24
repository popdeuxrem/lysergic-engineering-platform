from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


@dataclass
class KnowledgeEntry:
    entry_id: str
    kind: str
    content: str
    tags: tuple[str, ...] = ()
    source: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


class KnowledgeAPIProtocol(Protocol):
    def add(self, entry_id: str, kind: str, content: str, **kwargs: Any) -> KnowledgeEntry: ...

    def get(self, entry_id: str) -> KnowledgeEntry | None: ...

    def search(self, kind: str | None = None, tag: str | None = None) -> tuple[KnowledgeEntry, ...]: ...

    def remove(self, entry_id: str) -> bool: ...

    def count(self, kind: str | None = None) -> int: ...


class KnowledgeAPI:
    service_id = "api.knowledge"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._entries: dict[str, KnowledgeEntry] = {}

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._entries.clear()

    def add(self, entry_id: str, kind: str, content: str, **kwargs: Any) -> KnowledgeEntry:
        entry = KnowledgeEntry(entry_id=entry_id, kind=kind, content=content, **kwargs)
        self._entries[entry_id] = entry
        return entry

    def get(self, entry_id: str) -> KnowledgeEntry | None:
        return self._entries.get(entry_id)

    def search(self, kind: str | None = None, tag: str | None = None) -> tuple[KnowledgeEntry, ...]:
        results = list(self._entries.values())
        if kind is not None:
            results = [e for e in results if e.kind == kind]
        if tag is not None:
            results = [e for e in results if tag in e.tags]
        return tuple(results)

    def remove(self, entry_id: str) -> bool:
        if entry_id in self._entries:
            del self._entries[entry_id]
            return True
        return False

    def count(self, kind: str | None = None) -> int:
        if kind is None:
            return len(self._entries)
        return sum(1 for e in self._entries.values() if e.kind == kind)


def create_knowledge_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(
        service_id="api.knowledge",
        factory=lambda: KnowledgeAPI(manager),
    )
