from __future__ import annotations

from typing import Any

from runtime.knowledge.catalog import KnowledgeCatalog
from runtime.knowledge.events import KnowledgeEventPublisher
from runtime.knowledge.ingestion import KnowledgeIngestion
from runtime.knowledge.lifecycle import KnowledgeLifecycle, KnowledgeLifecycleState
from runtime.knowledge.model import KnowledgeItem, KnowledgeMetadata, KnowledgeSource
from runtime.knowledge.provenance import ProvenanceTracker
from runtime.knowledge.registry import KnowledgeRegistry
from runtime.knowledge.resolver import KnowledgeResolver
from runtime.knowledge.search import KnowledgeSearch
from runtime.knowledge.snapshot import KnowledgeSnapshot
from runtime.knowledge.validator import KnowledgeValidator
from runtime.services.events import EventBus
from runtime.services.registry import ServiceStatus


class KnowledgeManager:
    service_id = "knowledge.manager"
    dependencies: tuple[str, ...] = ()

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._registry = KnowledgeRegistry()
        self._lifecycle = KnowledgeLifecycle()
        self._catalog = KnowledgeCatalog()
        self._search = KnowledgeSearch(self._catalog)
        self._resolver = KnowledgeResolver(self._registry)
        self._ingestion = KnowledgeIngestion()
        self._validator = KnowledgeValidator()
        self._provenance = ProvenanceTracker()
        self._events = KnowledgeEventPublisher(event_bus)
        self._snapshot_version = 0
        self._snapshot: KnowledgeSnapshot | None = None
        self._initialized = False

    @property
    def registry(self) -> KnowledgeRegistry:
        return self._registry

    @property
    def lifecycle(self) -> KnowledgeLifecycle:
        return self._lifecycle

    @property
    def catalog(self) -> KnowledgeCatalog:
        return self._catalog

    @property
    def search(self) -> KnowledgeSearch:
        return self._search

    @property
    def provenance(self) -> ProvenanceTracker:
        return self._provenance

    @property
    def snapshot(self) -> KnowledgeSnapshot | None:
        return self._snapshot

    @property
    def manager_status(self) -> ServiceStatus:
        return ServiceStatus.READY if self._initialized else ServiceStatus.PENDING

    def initialize_runtime(self) -> None:
        if self._initialized:
            return
        self._snapshot_version = 0
        self._initialized = True
        self._freeze_snapshot()

    def shutdown(self) -> None:
        self._registry = KnowledgeRegistry()
        self._snapshot = None
        self._initialized = False

    def create(self, knowledge_id: str, title: str, kind: str, content: str = "", **kwargs: Any) -> KnowledgeItem:
        meta = KnowledgeMetadata(knowledge_id=knowledge_id, title=title, kind=kind, **{k: v for k, v in kwargs.items() if k in ("version", "description", "author", "tags")})
        item = KnowledgeItem(knowledge_id=knowledge_id, title=title, kind=kind, content=content, metadata=meta, **{k: v for k, v in kwargs.items() if k in ("version", "tags", "description", "author")})
        self._registry.register(item)
        self._lifecycle.initialize(knowledge_id)
        self._catalog.index(meta)
        self._provenance.record(item, origin="direct_creation")
        self._events.created(knowledge_id)
        self._freeze_snapshot()
        return item

    def get(self, knowledge_id: str) -> KnowledgeItem | None:
        return self._registry.get(knowledge_id)

    def list(self) -> tuple[KnowledgeItem, ...]:
        return self._registry.list()

    def ingest(self, knowledge_id: str, source: KnowledgeSource) -> KnowledgeItem | None:
        item = self._registry.get(knowledge_id)
        if item is None:
            return None
        self._ingestion.ingest(item, source)
        self._lifecycle.transition(knowledge_id, KnowledgeLifecycleState.INGESTED)
        self._provenance.add_transformation(knowledge_id, f"ingested_from:{source.source_type}")
        self._provenance.update_source(knowledge_id, item)
        self._events.ingested(knowledge_id)
        self._freeze_snapshot()
        return item

    def validate_item(self, knowledge_id: str) -> KnowledgeItem | None:
        item = self._registry.get(knowledge_id)
        if item is None:
            return None
        vr = self._validator.validate_tier1(item)
        if vr.valid:
            vr2 = self._validator.validate_tier2(item)
            if vr2.valid:
                self._lifecycle.transition(knowledge_id, KnowledgeLifecycleState.VALIDATED)
                self._events.validated(knowledge_id)
            else:
                self._lifecycle.transition(knowledge_id, KnowledgeLifecycleState.FAILED)
                self._events.failed(knowledge_id, "; ".join(vr2.errors))
        else:
            self._lifecycle.transition(knowledge_id, KnowledgeLifecycleState.FAILED)
            self._events.failed(knowledge_id, "; ".join(vr.errors))
        self._freeze_snapshot()
        return item

    def publish(self, knowledge_id: str) -> KnowledgeItem | None:
        item = self._registry.get(knowledge_id)
        if item is None:
            return None
        self._lifecycle.transition(knowledge_id, KnowledgeLifecycleState.AVAILABLE)
        self._events.published(knowledge_id)
        self._freeze_snapshot()
        return item

    def deprecate(self, knowledge_id: str) -> KnowledgeItem | None:
        item = self._registry.get(knowledge_id)
        if item is None:
            return None
        self._lifecycle.transition(knowledge_id, KnowledgeLifecycleState.DEPRECATED)
        self._events.deprecated(knowledge_id)
        self._freeze_snapshot()
        return item

    def archive_item(self, knowledge_id: str) -> KnowledgeItem | None:
        item = self._registry.get(knowledge_id)
        if item is None:
            return None
        self._lifecycle.transition(knowledge_id, KnowledgeLifecycleState.ARCHIVED)
        self._events.archived(knowledge_id)
        self._freeze_snapshot()
        return item

    def remove(self, knowledge_id: str) -> bool:
        if knowledge_id not in self._registry:
            return False
        self._registry.unregister(knowledge_id)
        self._catalog.remove(knowledge_id)
        self._freeze_snapshot()
        return True

    def search_items(self, query: str, kind: str | None = None) -> tuple[dict[str, Any], ...]:
        return self._search.search(query, kind)

    def resolve_urn(self, urn: str) -> KnowledgeItem | None:
        return self._resolver.resolve_urn(urn)

    def provenance_of(self, knowledge_id: str) -> dict[str, Any] | None:
        record = self._provenance.get(knowledge_id)
        return record.to_dict() if record else None

    def status(self, knowledge_id: str) -> str | None:
        state = self._lifecycle.state_of(knowledge_id)
        return state.value if state else None

    def snapshot_state(self) -> KnowledgeSnapshot:
        items = {i.knowledge_id: i for i in self._registry.list()}
        return KnowledgeSnapshot(items=items, version=self._snapshot_version)

    def _freeze_snapshot(self) -> None:
        self._snapshot_version += 1
        items = {i.knowledge_id: i for i in self._registry.list()}
        self._snapshot = KnowledgeSnapshot(items=items, version=self._snapshot_version)
