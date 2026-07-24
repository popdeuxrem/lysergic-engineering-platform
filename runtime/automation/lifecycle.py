from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any


class AutomationLifecycleState(Enum):
    CREATED = "created"
    VALIDATED = "validated"
    READY = "ready"
    ENABLED = "enabled"
    EXECUTING = "executing"
    DISABLED = "disabled"
    ARCHIVED = "archived"
    FAILED = "failed"


_AUTOMATION_TRANSITIONS: dict[AutomationLifecycleState, tuple[AutomationLifecycleState, ...]] = {
    AutomationLifecycleState.CREATED: (AutomationLifecycleState.VALIDATED, AutomationLifecycleState.FAILED, AutomationLifecycleState.ARCHIVED),
    AutomationLifecycleState.VALIDATED: (AutomationLifecycleState.READY, AutomationLifecycleState.FAILED, AutomationLifecycleState.ARCHIVED),
    AutomationLifecycleState.READY: (AutomationLifecycleState.ENABLED, AutomationLifecycleState.DISABLED, AutomationLifecycleState.ARCHIVED, AutomationLifecycleState.FAILED),
    AutomationLifecycleState.ENABLED: (AutomationLifecycleState.EXECUTING, AutomationLifecycleState.DISABLED, AutomationLifecycleState.FAILED),
    AutomationLifecycleState.EXECUTING: (AutomationLifecycleState.ENABLED, AutomationLifecycleState.DISABLED, AutomationLifecycleState.FAILED),
    AutomationLifecycleState.DISABLED: (AutomationLifecycleState.ENABLED, AutomationLifecycleState.ARCHIVED, AutomationLifecycleState.FAILED, AutomationLifecycleState.READY),
    AutomationLifecycleState.ARCHIVED: (AutomationLifecycleState.CREATED,),
    AutomationLifecycleState.FAILED: (AutomationLifecycleState.CREATED, AutomationLifecycleState.ARCHIVED),
}


class AutomationLifecycle:
    def __init__(self) -> None:
        self._states: dict[str, AutomationLifecycleState] = {}
        self._transitions: list[dict[str, Any]] = []

    def initialize(self, automation_id: str) -> None:
        self._states[automation_id] = AutomationLifecycleState.CREATED
        self._record(automation_id, AutomationLifecycleState.CREATED)

    def transition(self, automation_id: str, target: AutomationLifecycleState) -> None:
        current = self._states.get(automation_id)
        if current is None:
            raise KeyError(f"Automation not found: {automation_id}")
        allowed = _AUTOMATION_TRANSITIONS.get(current, ())
        if target not in allowed:
            from runtime.automation.exceptions import InvalidLifecycleError
            raise InvalidLifecycleError(current.value, target.value)
        self._states[automation_id] = target
        self._record(automation_id, target)

    def state_of(self, automation_id: str) -> AutomationLifecycleState | None:
        return self._states.get(automation_id)

    def can_transition(self, automation_id: str, target: AutomationLifecycleState) -> bool:
        current = self._states.get(automation_id)
        return current is not None and target in _AUTOMATION_TRANSITIONS.get(current, ())

    @property
    def history(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._transitions)

    def _record(self, automation_id: str, state: AutomationLifecycleState) -> None:
        self._transitions.append({"automation_id": automation_id, "state": state.value, "timestamp": datetime.now(UTC).isoformat()})
