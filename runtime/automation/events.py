from __future__ import annotations

from runtime.services.events import Event, EventBus


class AutomationEventPublisher:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus

    def created(self, automation_id: str) -> None:
        self._publish("AutomationCreated", {"automation_id": automation_id})

    def validated(self, automation_id: str) -> None:
        self._publish("AutomationValidated", {"automation_id": automation_id})

    def enabled(self, automation_id: str) -> None:
        self._publish("AutomationEnabled", {"automation_id": automation_id})

    def triggered(self, automation_id: str, trigger_type: str) -> None:
        self._publish("AutomationTriggered", {"automation_id": automation_id, "trigger_type": trigger_type})

    def started(self, automation_id: str) -> None:
        self._publish("AutomationStarted", {"automation_id": automation_id})

    def completed(self, automation_id: str) -> None:
        self._publish("AutomationCompleted", {"automation_id": automation_id})

    def failed(self, automation_id: str, error: str) -> None:
        self._publish("AutomationFailed", {"automation_id": automation_id, "error": error})

    def disabled(self, automation_id: str) -> None:
        self._publish("AutomationDisabled", {"automation_id": automation_id})

    def _publish(self, event_type: str, payload: dict[str, str]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=f"automation.{event_type}", payload=payload, source="automation"))
