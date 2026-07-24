from __future__ import annotations

from datetime import UTC, datetime

from runtime.knowledge.exceptions import IngestionError
from runtime.knowledge.model import KnowledgeItem, KnowledgeSource


class KnowledgeIngestion:
    def __init__(self) -> None:
        self._ingested: dict[str, datetime] = {}

    def ingest(self, item: KnowledgeItem, source: KnowledgeSource) -> KnowledgeItem:
        if not source.source_id:
            raise IngestionError(source.name, "source_id is required")
        item.source = source
        self._ingested[item.knowledge_id] = datetime.now(UTC)
        return item

    def ingest_from_asset(self, item: KnowledgeItem, asset_id: str, asset_type: str) -> KnowledgeItem:
        source = KnowledgeSource(source_id=asset_id, source_type="asset", name=asset_type, reference=asset_id)
        return self.ingest(item, source)

    def ingest_from_project(self, item: KnowledgeItem, project_id: str) -> KnowledgeItem:
        source = KnowledgeSource(source_id=project_id, source_type="project", name=project_id, reference=project_id)
        return self.ingest(item, source)

    def is_ingested(self, knowledge_id: str) -> bool:
        return knowledge_id in self._ingested

    def ingested_at(self, knowledge_id: str) -> datetime | None:
        return self._ingested.get(knowledge_id)
