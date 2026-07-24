from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from runtime.knowledge.model import KnowledgeItem, KnowledgeSource


@dataclass
class ProvenanceRecord:
    knowledge_id: str
    origin: str
    source: KnowledgeSource | None = None
    creator: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    transformations: tuple[str, ...] = ()
    relationships: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "knowledge_id": self.knowledge_id,
            "origin": self.origin,
            "source": {"source_id": self.source.source_id, "source_type": self.source.source_type} if self.source else None,
            "creator": self.creator,
            "created_at": self.created_at.isoformat(),
            "transformations": list(self.transformations),
            "relationships": list(self.relationships),
        }


class ProvenanceTracker:
    def __init__(self) -> None:
        self._records: dict[str, ProvenanceRecord] = {}

    def record(self, item: KnowledgeItem, origin: str, creator: str = "") -> ProvenanceRecord:
        record = ProvenanceRecord(knowledge_id=item.knowledge_id, origin=origin, source=item.source, creator=creator)
        self._records[item.knowledge_id] = record
        return record

    def update_source(self, knowledge_id: str, item: KnowledgeItem) -> None:
        record = self._records.get(knowledge_id)
        if record is not None:
            object.__setattr__(record, "source", item.source)

    def add_transformation(self, knowledge_id: str, transformation: str) -> None:
        record = self._records.get(knowledge_id)
        if record is not None:
            record.transformations = record.transformations + (transformation,)

    def add_relationship(self, knowledge_id: str, relationship: str) -> None:
        record = self._records.get(knowledge_id)
        if record is not None:
            record.relationships = record.relationships + (relationship,)

    def get(self, knowledge_id: str) -> ProvenanceRecord | None:
        return self._records.get(knowledge_id)
