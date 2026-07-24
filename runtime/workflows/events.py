from __future__ import annotations

from runtime.services.events import Event, EventBus


class WorkflowEventPublisher:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus

    def created(self, workflow_id: str) -> None:
        self._publish("WorkflowCreated", {"workflow_id": workflow_id})

    def validated(self, workflow_id: str) -> None:
        self._publish("WorkflowValidated", {"workflow_id": workflow_id})

    def started(self, workflow_id: str) -> None:
        self._publish("WorkflowStarted", {"workflow_id": workflow_id})

    def step_started(self, workflow_id: str, step_id: str) -> None:
        self._publish("WorkflowStepStarted", {"workflow_id": workflow_id, "step_id": step_id})

    def step_completed(self, workflow_id: str, step_id: str) -> None:
        self._publish("WorkflowStepCompleted", {"workflow_id": workflow_id, "step_id": step_id})

    def completed(self, workflow_id: str) -> None:
        self._publish("WorkflowCompleted", {"workflow_id": workflow_id})

    def failed(self, workflow_id: str, error: str) -> None:
        self._publish("WorkflowFailed", {"workflow_id": workflow_id, "error": error})

    def stopped(self, workflow_id: str) -> None:
        self._publish("WorkflowStopped", {"workflow_id": workflow_id})

    def _publish(self, event_type: str, payload: dict[str, str]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=f"workflow.{event_type}", payload=payload, source="workflows"))
