from __future__ import annotations

from runtime.knowledge.exceptions import KnowledgeConflictError, RegistryFrozenError
from runtime.knowledge.model import KnowledgeItem


class KnowledgeRegistry:
    def __init__(self) -> None:
        self._items: dict[str, KnowledgeItem] = {}
        self._frozen = False

    def register(self, item: KnowledgeItem) -> None:
        if self._frozen:
            raise RegistryFrozenError()
        if item.knowledge_id in self._items:
            raise KnowledgeConflictError(item.knowledge_id)
        self._items[item.knowledge_id] = item

    def get(self, knowledge_id: str) -> KnowledgeItem | None:
        return self._items.get(knowledge_id)

    def unregister(self, knowledge_id: str) -> bool:
        if self._frozen:
            raise RegistryFrozenError()
        return self._items.pop(knowledge_id, None) is not None

    def list(self) -> tuple[KnowledgeItem, ...]:
        return tuple(self._items.values())

    def list_by_kind(self, kind: str) -> tuple[KnowledgeItem, ...]:
        return tuple(i for i in self._items.values() if i.kind == kind)

    def list_by_tag(self, tag: str) -> tuple[KnowledgeItem, ...]:
        return tuple(i for i in self._items.values() if tag in i.tags)

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def count(self) -> int:
        return len(self._items)

    def __contains__(self, knowledge_id: str) -> bool:
        return knowledge_id in self._items
