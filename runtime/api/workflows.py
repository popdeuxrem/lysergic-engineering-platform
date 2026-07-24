from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SCHEDULED = "scheduled"


@dataclass
class WorkflowRecord:
    workflow_id: str
    name: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    steps: tuple[str, ...] = ()
    current_step: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None
    scheduled_at: datetime | None = None
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class WorkflowAPIProtocol(Protocol):
    def create(self, workflow_id: str, name: str, steps: tuple[str, ...] = ()) -> WorkflowRecord: ...
    def get(self, workflow_id: str) -> WorkflowRecord | None: ...
    def list(self, status: WorkflowStatus | None = None) -> tuple[WorkflowRecord, ...]: ...
    def start(self, workflow_id: str) -> WorkflowRecord | None: ...
    def complete(self, workflow_id: str) -> WorkflowRecord | None: ...
    def fail(self, workflow_id: str, error: str) -> WorkflowRecord | None: ...
    def cancel(self, workflow_id: str) -> WorkflowRecord | None: ...
    def schedule(self, workflow_id: str, scheduled_at: datetime) -> WorkflowRecord | None: ...
    def history(self) -> tuple[WorkflowRecord, ...]: ...
    def list_scheduled(self) -> tuple[WorkflowRecord, ...]: ...
    def count(self) -> int: ...


class WorkflowAPI:
    service_id = "api.workflows"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._workflows: dict[str, WorkflowRecord] = {}
        self._history: list[WorkflowRecord] = []

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._workflows.clear()
        self._history.clear()

    def create(self, workflow_id: str, name: str, steps: tuple[str, ...] = ()) -> WorkflowRecord:
        record = WorkflowRecord(workflow_id=workflow_id, name=name, steps=steps)
        self._workflows[workflow_id] = record
        return record

    def get(self, workflow_id: str) -> WorkflowRecord | None:
        return self._workflows.get(workflow_id)

    def list(self, status: WorkflowStatus | None = None) -> tuple[WorkflowRecord, ...]:
        if status is None:
            return tuple(self._workflows.values())
        return tuple(w for w in self._workflows.values() if w.status == status)

    def start(self, workflow_id: str) -> WorkflowRecord | None:
        record = self._workflows.get(workflow_id)
        if record is None or record.status not in (WorkflowStatus.PENDING, WorkflowStatus.SCHEDULED):
            return None
        self._workflows[workflow_id] = WorkflowRecord(
            workflow_id=record.workflow_id, name=record.name,
            status=WorkflowStatus.RUNNING, steps=record.steps, current_step=0,
            created_at=record.created_at, started_at=datetime.now(UTC),
            scheduled_at=record.scheduled_at, metadata=record.metadata,
        )
        return self._workflows[workflow_id]

    def complete(self, workflow_id: str) -> WorkflowRecord | None:
        record = self._workflows.get(workflow_id)
        if record is None or record.status != WorkflowStatus.RUNNING:
            return None
        record = WorkflowRecord(
            workflow_id=record.workflow_id, name=record.name,
            status=WorkflowStatus.COMPLETED, steps=record.steps,
            current_step=len(record.steps), created_at=record.created_at,
            started_at=record.started_at, completed_at=datetime.now(UTC),
            scheduled_at=record.scheduled_at, metadata=record.metadata,
        )
        self._workflows[workflow_id] = record
        self._history.append(record)
        return record

    def fail(self, workflow_id: str, error: str) -> WorkflowRecord | None:
        record = self._workflows.get(workflow_id)
        if record is None or record.status not in (WorkflowStatus.RUNNING, WorkflowStatus.PENDING):
            return None
        record = WorkflowRecord(
            workflow_id=record.workflow_id, name=record.name,
            status=WorkflowStatus.FAILED, steps=record.steps,
            created_at=record.created_at, started_at=record.started_at,
            scheduled_at=record.scheduled_at, error=error, metadata=record.metadata,
        )
        self._workflows[workflow_id] = record
        self._history.append(record)
        return record

    def cancel(self, workflow_id: str) -> WorkflowRecord | None:
        record = self._workflows.get(workflow_id)
        if record is None or record.status not in (WorkflowStatus.PENDING, WorkflowStatus.RUNNING, WorkflowStatus.SCHEDULED):
            return None
        record = WorkflowRecord(
            workflow_id=record.workflow_id, name=record.name,
            status=WorkflowStatus.CANCELLED, steps=record.steps,
            created_at=record.created_at, started_at=record.started_at,
            scheduled_at=record.scheduled_at, metadata=record.metadata,
        )
        self._workflows[workflow_id] = record
        self._history.append(record)
        return record

    def schedule(self, workflow_id: str, scheduled_at: datetime) -> WorkflowRecord | None:
        record = self._workflows.get(workflow_id)
        if record is None or record.status != WorkflowStatus.PENDING:
            return None
        self._workflows[workflow_id] = WorkflowRecord(
            workflow_id=record.workflow_id, name=record.name,
            status=WorkflowStatus.SCHEDULED, steps=record.steps,
            created_at=record.created_at, scheduled_at=scheduled_at, metadata=record.metadata,
        )
        return self._workflows[workflow_id]

    def history(self) -> tuple[WorkflowRecord, ...]:
        return tuple(self._history)

    def list_scheduled(self) -> tuple[WorkflowRecord, ...]:
        return self.list(WorkflowStatus.SCHEDULED)

    def count(self) -> int:
        return len(self._workflows)


def create_workflow_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(service_id="api.workflows", factory=lambda: WorkflowAPI(manager))
