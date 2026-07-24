from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.knowledge.model import KnowledgeItem


class KnowledgeSnapshot:
    def __init__(self, items: dict[str, KnowledgeItem], version: int = 0) -> None:
        self._items = dict(items)
        self._version = version
        self._timestamp = datetime.now(UTC)

    def get(self, knowledge_id: str) -> KnowledgeItem | None:
        return self._items.get(knowledge_id)

    def list(self) -> tuple[KnowledgeItem, ...]:
        return tuple(self._items.values())

    def count(self) -> int:
        return len(self._items)

    @property
    def version(self) -> int:
        return self._version

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> dict[str, Any]:
        return {"version": self._version, "timestamp": self._timestamp.isoformat(), "items": [i.knowledge_id for i in self._items.values()]}
