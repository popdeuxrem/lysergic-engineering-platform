from __future__ import annotations

from runtime.services.events import Event, EventBus


class KnowledgeEventPublisher:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus

    def created(self, knowledge_id: str) -> None:
        self._publish("KnowledgeCreated", {"knowledge_id": knowledge_id})

    def ingested(self, knowledge_id: str) -> None:
        self._publish("KnowledgeIngested", {"knowledge_id": knowledge_id})

    def validated(self, knowledge_id: str) -> None:
        self._publish("KnowledgeValidated", {"knowledge_id": knowledge_id})

    def published(self, knowledge_id: str) -> None:
        self._publish("KnowledgePublished", {"knowledge_id": knowledge_id})

    def deprecated(self, knowledge_id: str) -> None:
        self._publish("KnowledgeDeprecated", {"knowledge_id": knowledge_id})

    def archived(self, knowledge_id: str) -> None:
        self._publish("KnowledgeArchived", {"knowledge_id": knowledge_id})

    def failed(self, knowledge_id: str, error: str) -> None:
        self._publish("KnowledgeFailed", {"knowledge_id": knowledge_id, "error": error})

    def _publish(self, event_type: str, payload: dict[str, str]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=f"knowledge.{event_type}", payload=payload, source="knowledge"))
