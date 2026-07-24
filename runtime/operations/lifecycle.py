from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any


class OperationLifecycleState(Enum):
    CREATED = "created"
    DEFINED = "defined"
    VALIDATED = "validated"
    READY = "ready"
    EXECUTING = "executing"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    FAILED = "failed"


_OP_TRANSITIONS: dict[OperationLifecycleState, tuple[OperationLifecycleState, ...]] = {
    OperationLifecycleState.CREATED: (OperationLifecycleState.DEFINED, OperationLifecycleState.FAILED, OperationLifecycleState.ARCHIVED),
    OperationLifecycleState.DEFINED: (OperationLifecycleState.VALIDATED, OperationLifecycleState.FAILED, OperationLifecycleState.ARCHIVED),
    OperationLifecycleState.VALIDATED: (OperationLifecycleState.READY, OperationLifecycleState.FAILED, OperationLifecycleState.ARCHIVED),
    OperationLifecycleState.READY: (OperationLifecycleState.EXECUTING, OperationLifecycleState.ARCHIVED, OperationLifecycleState.FAILED),
    OperationLifecycleState.EXECUTING: (OperationLifecycleState.COMPLETED, OperationLifecycleState.FAILED),
    OperationLifecycleState.COMPLETED: (OperationLifecycleState.ARCHIVED,),
    OperationLifecycleState.ARCHIVED: (OperationLifecycleState.CREATED,),
    OperationLifecycleState.FAILED: (OperationLifecycleState.CREATED, OperationLifecycleState.ARCHIVED),
}


class OperationLifecycle:
    def __init__(self) -> None:
        self._states: dict[str, OperationLifecycleState] = {}
        self._transitions: list[dict[str, Any]] = []

    def initialize(self, op_id: str) -> None:
        self._states[op_id] = OperationLifecycleState.CREATED
        self._record(op_id, OperationLifecycleState.CREATED)

    def transition(self, op_id: str, target: OperationLifecycleState) -> None:
        current = self._states.get(op_id)
        if current is None:
            raise KeyError(f"Operation not found: {op_id}")
        allowed = _OP_TRANSITIONS.get(current, ())
        if target not in allowed:
            from runtime.operations.exceptions import InvalidLifecycleError
            raise InvalidLifecycleError(current.value, target.value)
        self._states[op_id] = target
        self._record(op_id, target)

    def state_of(self, op_id: str) -> OperationLifecycleState | None:
        return self._states.get(op_id)

    def can_transition(self, op_id: str, target: OperationLifecycleState) -> bool:
        current = self._states.get(op_id)
        return current is not None and target in _OP_TRANSITIONS.get(current, ())

    @property
    def history(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._transitions)

    def _record(self, op_id: str, state: OperationLifecycleState) -> None:
        self._transitions.append({"operation_id": op_id, "state": state.value, "timestamp": datetime.now(UTC).isoformat()})
