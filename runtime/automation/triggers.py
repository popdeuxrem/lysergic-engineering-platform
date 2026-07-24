from __future__ import annotations

from typing import Any

from runtime.automation.model import TriggerDefinition


class TriggerRegistry:
    def __init__(self) -> None:
        self._requests: list[TriggerDefinition] = []

    def evaluate(self, trigger: TriggerDefinition) -> bool:
        return trigger.trigger_type in ("event", "schedule", "manual")

    def request_execution(self, trigger: TriggerDefinition) -> None:
        self._requests.append(trigger)

    def pending_requests(self) -> tuple[TriggerDefinition, ...]:
        requests = tuple(self._requests)
        self._requests.clear()
        return requests

    @property
    def request_count(self) -> int:
        return len(self._requests)


class EventTrigger:
    trigger_type = "event"

    def __init__(self, source: str = "") -> None:
        self.source = source

    def create_definition(self, trigger_id: str, source: str = "", config: dict[str, Any] | None = None) -> TriggerDefinition:
        return TriggerDefinition(trigger_id=trigger_id, trigger_type="event", source=source or self.source, config=config or {})


class ScheduleTrigger:
    trigger_type = "schedule"

    def __init__(self, cron: str = "") -> None:
        self.cron = cron

    def create_definition(self, trigger_id: str, cron: str = "", config: dict[str, Any] | None = None) -> TriggerDefinition:
        return TriggerDefinition(trigger_id=trigger_id, trigger_type="schedule", config={"cron": cron or self.cron, **(config or {})})


class ManualTrigger:
    trigger_type = "manual"

    def create_definition(self, trigger_id: str, config: dict[str, Any] | None = None) -> TriggerDefinition:
        return TriggerDefinition(trigger_id=trigger_id, trigger_type="manual", config=config or {})
