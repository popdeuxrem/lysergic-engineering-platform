from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any


class RuntimeLifecycleState(Enum):
    INSTALLED = "installed"
    DISCOVERED = "discovered"
    VALIDATED = "validated"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    EXECUTING = "executing"
    SHUTDOWN = "shutdown"
    REMOVED = "removed"
    FAILED = "failed"


_RUNTIME_TRANSITIONS: dict[RuntimeLifecycleState, tuple[RuntimeLifecycleState, ...]] = {
    RuntimeLifecycleState.INSTALLED: (RuntimeLifecycleState.DISCOVERED, RuntimeLifecycleState.FAILED, RuntimeLifecycleState.REMOVED),
    RuntimeLifecycleState.DISCOVERED: (RuntimeLifecycleState.VALIDATED, RuntimeLifecycleState.FAILED, RuntimeLifecycleState.REMOVED),
    RuntimeLifecycleState.VALIDATED: (RuntimeLifecycleState.LOADED, RuntimeLifecycleState.FAILED, RuntimeLifecycleState.REMOVED),
    RuntimeLifecycleState.LOADED: (RuntimeLifecycleState.INITIALIZED, RuntimeLifecycleState.FAILED, RuntimeLifecycleState.REMOVED),
    RuntimeLifecycleState.INITIALIZED: (RuntimeLifecycleState.EXECUTING, RuntimeLifecycleState.SHUTDOWN, RuntimeLifecycleState.FAILED),
    RuntimeLifecycleState.EXECUTING: (RuntimeLifecycleState.SHUTDOWN, RuntimeLifecycleState.FAILED),
    RuntimeLifecycleState.SHUTDOWN: (RuntimeLifecycleState.REMOVED, RuntimeLifecycleState.FAILED, RuntimeLifecycleState.INSTALLED),
    RuntimeLifecycleState.REMOVED: (),
    RuntimeLifecycleState.FAILED: (RuntimeLifecycleState.REMOVED, RuntimeLifecycleState.INSTALLED),
}


class ExtensionRuntimeLifecycle:
    def __init__(self) -> None:
        self._states: dict[str, RuntimeLifecycleState] = {}
        self._transitions: list[dict[str, Any]] = []

    def install(self, extension_id: str) -> None:
        self._states[extension_id] = RuntimeLifecycleState.INSTALLED
        self._record(extension_id, RuntimeLifecycleState.INSTALLED)

    def transition(self, extension_id: str, target: RuntimeLifecycleState) -> None:
        current = self._states.get(extension_id)
        if current is None:
            raise KeyError(f"Extension not found: {extension_id}")
        allowed = _RUNTIME_TRANSITIONS.get(current, ())
        if target not in allowed:
            from runtime.extensions.exceptions import InvalidLifecycleTransitionError
            raise InvalidLifecycleTransitionError(current.value, target.value)
        self._states[extension_id] = target
        self._record(extension_id, target)

    def state_of(self, extension_id: str) -> RuntimeLifecycleState | None:
        return self._states.get(extension_id)

    def can_transition(self, extension_id: str, target: RuntimeLifecycleState) -> bool:
        current = self._states.get(extension_id)
        return current is not None and target in _RUNTIME_TRANSITIONS.get(current, ())

    @property
    def history(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._transitions)

    def _record(self, extension_id: str, state: RuntimeLifecycleState) -> None:
        self._transitions.append({"extension_id": extension_id, "state": state.value, "timestamp": datetime.now(UTC).isoformat()})
