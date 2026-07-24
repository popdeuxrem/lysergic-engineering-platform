from __future__ import annotations

from typing import Any

from runtime.knowledge.model import KnowledgeMetadata


class KnowledgeCatalog:
    def __init__(self) -> None:
        self._entries: dict[str, dict[str, Any]] = {}

    def index(self, metadata: KnowledgeMetadata) -> None:
        self._entries[metadata.knowledge_id] = {
            "knowledge_id": metadata.knowledge_id,
            "title": metadata.title,
            "kind": metadata.kind,
            "version": metadata.version,
            "description": metadata.description,
            "author": metadata.author,
            "tags": metadata.tags,
        }

    def remove(self, knowledge_id: str) -> bool:
        return self._entries.pop(knowledge_id, None) is not None

    def get(self, knowledge_id: str) -> dict[str, Any] | None:
        return self._entries.get(knowledge_id)

    def filter(self, kind: str | None = None, tag: str | None = None) -> tuple[dict[str, Any], ...]:
        results = list(self._entries.values())
        if kind is not None:
            results = [r for r in results if r["kind"] == kind]
        if tag is not None:
            results = [r for r in results if tag in r["tags"]]
        return tuple(results)

    @property
    def entries(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._entries.values())

    @property
    def count(self) -> int:
        return len(self._entries)
