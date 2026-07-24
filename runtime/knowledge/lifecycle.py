from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any


class KnowledgeLifecycleState(Enum):
    CREATED = "created"
    INGESTED = "ingested"
    VALIDATED = "validated"
    AVAILABLE = "available"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    FAILED = "failed"


_KNOWLEDGE_TRANSITIONS: dict[KnowledgeLifecycleState, tuple[KnowledgeLifecycleState, ...]] = {
    KnowledgeLifecycleState.CREATED: (KnowledgeLifecycleState.INGESTED, KnowledgeLifecycleState.FAILED, KnowledgeLifecycleState.ARCHIVED),
    KnowledgeLifecycleState.INGESTED: (KnowledgeLifecycleState.VALIDATED, KnowledgeLifecycleState.FAILED, KnowledgeLifecycleState.ARCHIVED),
    KnowledgeLifecycleState.VALIDATED: (KnowledgeLifecycleState.AVAILABLE, KnowledgeLifecycleState.FAILED, KnowledgeLifecycleState.ARCHIVED),
    KnowledgeLifecycleState.AVAILABLE: (KnowledgeLifecycleState.DEPRECATED, KnowledgeLifecycleState.ARCHIVED, KnowledgeLifecycleState.FAILED),
    KnowledgeLifecycleState.DEPRECATED: (KnowledgeLifecycleState.ARCHIVED, KnowledgeLifecycleState.FAILED),
    KnowledgeLifecycleState.ARCHIVED: (KnowledgeLifecycleState.AVAILABLE,),
    KnowledgeLifecycleState.FAILED: (KnowledgeLifecycleState.CREATED, KnowledgeLifecycleState.ARCHIVED),
}


class KnowledgeLifecycle:
    def __init__(self) -> None:
        self._states: dict[str, KnowledgeLifecycleState] = {}
        self._transitions: list[dict[str, Any]] = []

    def initialize(self, knowledge_id: str) -> None:
        self._states[knowledge_id] = KnowledgeLifecycleState.CREATED
        self._record(knowledge_id, KnowledgeLifecycleState.CREATED)

    def transition(self, knowledge_id: str, target: KnowledgeLifecycleState) -> None:
        current = self._states.get(knowledge_id)
        if current is None:
            raise KeyError(f"Knowledge not found: {knowledge_id}")
        allowed = _KNOWLEDGE_TRANSITIONS.get(current, ())
        if target not in allowed:
            from runtime.knowledge.exceptions import InvalidLifecycleTransitionError
            raise InvalidLifecycleTransitionError(current.value, target.value)
        self._states[knowledge_id] = target
        self._record(knowledge_id, target)

    def state_of(self, knowledge_id: str) -> KnowledgeLifecycleState | None:
        return self._states.get(knowledge_id)

    def can_transition(self, knowledge_id: str, target: KnowledgeLifecycleState) -> bool:
        current = self._states.get(knowledge_id)
        return current is not None and target in _KNOWLEDGE_TRANSITIONS.get(current, ())

    @property
    def history(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._transitions)

    def _record(self, knowledge_id: str, state: KnowledgeLifecycleState) -> None:
        self._transitions.append({"knowledge_id": knowledge_id, "state": state.value, "timestamp": datetime.now(UTC).isoformat()})
