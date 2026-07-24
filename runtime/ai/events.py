from __future__ import annotations

from runtime.services.events import Event, EventBus


class AIEventPublisher:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus

    def created(self, agent_id: str) -> None:
        self._publish("AgentCreated", {"agent_id": agent_id})

    def registered(self, agent_id: str) -> None:
        self._publish("AgentRegistered", {"agent_id": agent_id})

    def validated(self, agent_id: str) -> None:
        self._publish("AgentValidated", {"agent_id": agent_id})

    def started(self, agent_id: str) -> None:
        self._publish("AgentStarted", {"agent_id": agent_id})

    def execution_started(self, agent_id: str, execution_id: str) -> None:
        self._publish("AgentExecutionStarted", {"agent_id": agent_id, "execution_id": execution_id})

    def execution_completed(self, agent_id: str, execution_id: str) -> None:
        self._publish("AgentExecutionCompleted", {"agent_id": agent_id, "execution_id": execution_id})

    def failed(self, agent_id: str, error: str) -> None:
        self._publish("AgentFailed", {"agent_id": agent_id, "error": error})

    def stopped(self, agent_id: str) -> None:
        self._publish("AgentStopped", {"agent_id": agent_id})

    def _publish(self, event_type: str, payload: dict[str, str]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=f"ai.{event_type}", payload=payload, source="ai"))
