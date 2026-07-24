from __future__ import annotations

from runtime.services.events import Event, EventBus


class OperationsEventPublisher:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus

    def created(self, op_id: str) -> None:
        self._publish("OperationCreated", {"operation_id": op_id})

    def validated(self, op_id: str) -> None:
        self._publish("OperationValidated", {"operation_id": op_id})

    def prepared(self, op_id: str) -> None:
        self._publish("OperationPrepared", {"operation_id": op_id})

    def started(self, op_id: str) -> None:
        self._publish("OperationStarted", {"operation_id": op_id})

    def gate_passed(self, op_id: str, gate_id: str) -> None:
        self._publish("OperationGatePassed", {"operation_id": op_id, "gate_id": gate_id})

    def gate_failed(self, op_id: str, gate_id: str) -> None:
        self._publish("OperationGateFailed", {"operation_id": op_id, "gate_id": gate_id})

    def completed(self, op_id: str) -> None:
        self._publish("OperationCompleted", {"operation_id": op_id})

    def failed(self, op_id: str, error: str) -> None:
        self._publish("OperationFailed", {"operation_id": op_id, "error": error})

    def _publish(self, event_type: str, payload: dict[str, str]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=f"ops.{event_type}", payload=payload, source="operations"))
