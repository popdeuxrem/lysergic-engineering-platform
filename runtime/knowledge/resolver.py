from __future__ import annotations

from runtime.knowledge.model import KnowledgeItem
from runtime.knowledge.registry import KnowledgeRegistry


class KnowledgeResolver:
    def __init__(self, registry: KnowledgeRegistry) -> None:
        self._registry = registry

    def resolve_urn(self, urn: str) -> KnowledgeItem | None:
        if not urn.startswith("urn:lep:knowledge:"):
            return None
        parts = urn.split(":")
        if len(parts) < 4:
            return None
        knowledge_id = parts[3]
        return self._registry.get(knowledge_id)

    def resolve(self, knowledge_id: str) -> KnowledgeItem | None:
        return self._registry.get(knowledge_id)
