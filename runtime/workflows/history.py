from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from runtime.workflows.model import WorkflowResult


@dataclass
class ExecutionRecord:
    execution_id: str
    workflow_id: str
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    step_results: tuple[dict[str, Any], ...] = ()
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_id,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "step_results": list(self.step_results),
            "error": self.error,
        }


class WorkflowHistory:
    def __init__(self) -> None:
        self._records: dict[str, list[ExecutionRecord]] = {}
        self._all_records: list[ExecutionRecord] = []

    def record(self, result: WorkflowResult) -> None:
        record = ExecutionRecord(
            execution_id=result.execution_id, workflow_id=result.workflow_id,
            status=result.status, started_at=result.started_at, completed_at=result.completed_at,
            step_results=tuple(sr.__dict__ for sr in result.step_results), error=result.error,
        )
        if result.workflow_id not in self._records:
            self._records[result.workflow_id] = []
        self._records[result.workflow_id].append(record)
        self._all_records.append(record)

    def get(self, workflow_id: str) -> tuple[ExecutionRecord, ...]:
        return tuple(self._records.get(workflow_id, []))

    def get_execution(self, execution_id: str) -> ExecutionRecord | None:
        for record in self._all_records:
            if record.execution_id == execution_id:
                return record
        return None

    @property
    def all(self) -> tuple[ExecutionRecord, ...]:
        return tuple(self._all_records)

    @property
    def count(self) -> int:
        return len(self._all_records)
