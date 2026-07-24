from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


@dataclass
class KnowledgeSource:
    source_id: str
    name: str
    kind: str = ""
    enabled: bool = True
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class KnowledgeEntry:
    entry_id: str
    kind: str
    content: str
    tags: tuple[str, ...] = ()
    source: str = ""
    indexed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


class KnowledgeAPIProtocol(Protocol):
    def register_source(self, source_id: str, name: str, **kwargs: Any) -> KnowledgeSource: ...
    def sources(self) -> tuple[KnowledgeSource, ...]: ...
    def add(self, entry_id: str, kind: str, content: str, **kwargs: Any) -> KnowledgeEntry: ...
    def get(self, entry_id: str) -> KnowledgeEntry | None: ...
    def search(self, kind: str | None = None, tag: str | None = None, query: str | None = None) -> tuple[KnowledgeEntry, ...]: ...
    def index(self, entry_id: str) -> KnowledgeEntry | None: ...
    def remove(self, entry_id: str) -> bool: ...
    def count(self, kind: str | None = None) -> int: ...


class KnowledgeAPI:
    service_id = "api.knowledge"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._sources: dict[str, KnowledgeSource] = {}
        self._entries: dict[str, KnowledgeEntry] = {}

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._sources.clear()
        self._entries.clear()

    def register_source(self, source_id: str, name: str, **kwargs: Any) -> KnowledgeSource:
        source = KnowledgeSource(source_id=source_id, name=name, **kwargs)
        self._sources[source_id] = source
        return source

    def sources(self) -> tuple[KnowledgeSource, ...]:
        return tuple(self._sources.values())

    def add(self, entry_id: str, kind: str, content: str, **kwargs: Any) -> KnowledgeEntry:
        entry = KnowledgeEntry(entry_id=entry_id, kind=kind, content=content, **kwargs)
        self._entries[entry_id] = entry
        return entry

    def get(self, entry_id: str) -> KnowledgeEntry | None:
        return self._entries.get(entry_id)

    def search(self, kind: str | None = None, tag: str | None = None, query: str | None = None) -> tuple[KnowledgeEntry, ...]:
        results = list(self._entries.values())
        if kind is not None:
            results = [e for e in results if e.kind == kind]
        if tag is not None:
            results = [e for e in results if tag in e.tags]
        if query is not None:
            q = query.lower()
            results = [e for e in results if q in e.content.lower() or q in e.entry_id.lower()]
        return tuple(results)

    def index(self, entry_id: str) -> KnowledgeEntry | None:
        entry = self._entries.get(entry_id)
        if entry is None:
            return None
        self._entries[entry_id] = KnowledgeEntry(
            entry_id=entry.entry_id, kind=entry.kind, content=entry.content,
            tags=entry.tags, source=entry.source, indexed_at=datetime.now(UTC),
            created_at=entry.created_at, metadata=entry.metadata,
        )
        return self._entries[entry_id]

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
    return ServiceDefinition(service_id="api.knowledge", factory=lambda: KnowledgeAPI(manager))
