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


@dataclass
class WorkflowRecord:
    workflow_id: str
    name: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    steps: tuple[str, ...] = ()
    current_step: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None
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

    def count(self) -> int: ...


class WorkflowAPI:
    service_id = "api.workflows"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._workflows: dict[str, WorkflowRecord] = {}

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._workflows.clear()

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
        if record is None or record.status != WorkflowStatus.PENDING:
            return None
        self._workflows[workflow_id] = WorkflowRecord(
            workflow_id=record.workflow_id,
            name=record.name,
            status=WorkflowStatus.RUNNING,
            steps=record.steps,
            current_step=0,
            created_at=record.created_at,
            metadata=record.metadata,
        )
        return self._workflows[workflow_id]

    def complete(self, workflow_id: str) -> WorkflowRecord | None:
        record = self._workflows.get(workflow_id)
        if record is None or record.status != WorkflowStatus.RUNNING:
            return None
        self._workflows[workflow_id] = WorkflowRecord(
            workflow_id=record.workflow_id,
            name=record.name,
            status=WorkflowStatus.COMPLETED,
            steps=record.steps,
            current_step=len(record.steps),
            created_at=record.created_at,
            completed_at=datetime.now(UTC),
            metadata=record.metadata,
        )
        return self._workflows[workflow_id]

    def fail(self, workflow_id: str, error: str) -> WorkflowRecord | None:
        record = self._workflows.get(workflow_id)
        if record is None or record.status not in (WorkflowStatus.RUNNING, WorkflowStatus.PENDING):
            return None
        self._workflows[workflow_id] = WorkflowRecord(
            workflow_id=record.workflow_id,
            name=record.name,
            status=WorkflowStatus.FAILED,
            steps=record.steps,
            created_at=record.created_at,
            error=error,
            metadata=record.metadata,
        )
        return self._workflows[workflow_id]

    def cancel(self, workflow_id: str) -> WorkflowRecord | None:
        record = self._workflows.get(workflow_id)
        if record is None or record.status not in (WorkflowStatus.PENDING, WorkflowStatus.RUNNING):
            return None
        self._workflows[workflow_id] = WorkflowRecord(
            workflow_id=record.workflow_id,
            name=record.name,
            status=WorkflowStatus.CANCELLED,
            steps=record.steps,
            created_at=record.created_at,
            metadata=record.metadata,
        )
        return self._workflows[workflow_id]

    def count(self) -> int:
        return len(self._workflows)


def create_workflow_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(
        service_id="api.workflows",
        factory=lambda: WorkflowAPI(manager),
    )
