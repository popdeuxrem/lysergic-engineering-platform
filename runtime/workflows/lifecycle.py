from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any


class WorkflowStatus(Enum):
    CREATED = "created"
    VALIDATED = "validated"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


_WF_TRANSITIONS: dict[WorkflowStatus, tuple[WorkflowStatus, ...]] = {
    WorkflowStatus.CREATED: (WorkflowStatus.VALIDATED, WorkflowStatus.FAILED),
    WorkflowStatus.VALIDATED: (WorkflowStatus.READY, WorkflowStatus.FAILED),
    WorkflowStatus.READY: (WorkflowStatus.RUNNING,),
    WorkflowStatus.RUNNING: (WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.STOPPED),
    WorkflowStatus.COMPLETED: (),
    WorkflowStatus.FAILED: (WorkflowStatus.CREATED,),
    WorkflowStatus.STOPPED: (WorkflowStatus.CREATED,),
}


class WorkflowLifecycle:
    def __init__(self) -> None:
        self._states: dict[str, WorkflowStatus] = {}
        self._transitions: list[dict[str, Any]] = []

    def initialize(self, workflow_id: str) -> WorkflowStatus:
        self._states[workflow_id] = WorkflowStatus.CREATED
        self._record(workflow_id, WorkflowStatus.CREATED)
        return WorkflowStatus.CREATED

    def transition(self, workflow_id: str, target: WorkflowStatus) -> WorkflowStatus:
        current = self._states.get(workflow_id)
        if current is None:
            raise KeyError(f"Workflow not found: {workflow_id}")
        allowed = _WF_TRANSITIONS.get(current, ())
        if target not in allowed:
            from runtime.workflows.exceptions import InvalidTransitionError
            raise InvalidTransitionError(current.value, target.value)
        self._states[workflow_id] = target
        self._record(workflow_id, target)
        return target

    def state_of(self, workflow_id: str) -> WorkflowStatus | None:
        return self._states.get(workflow_id)

    def can_transition(self, workflow_id: str, target: WorkflowStatus) -> bool:
        current = self._states.get(workflow_id)
        if current is None:
            return False
        allowed = _WF_TRANSITIONS.get(current, ())
        return target in allowed

    @property
    def history(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._transitions)

    def _record(self, workflow_id: str, status: WorkflowStatus) -> None:
        self._transitions.append({
            "workflow_id": workflow_id, "status": status.value, "timestamp": datetime.now(UTC).isoformat(),
        })
