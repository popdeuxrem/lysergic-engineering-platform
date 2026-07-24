from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from runtime.operations.model import OperationExecution


@dataclass
class HistoryRecord:
    execution_id: str
    operation_id: str
    version: str
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"execution_id": self.execution_id, "operation_id": self.operation_id, "version": self.version, "status": self.status, "started_at": self.started_at.isoformat() if self.started_at else None, "completed_at": self.completed_at.isoformat() if self.completed_at else None, "error": self.error}


class OperationsHistory:
    def __init__(self) -> None:
        self._records: list[HistoryRecord] = []

    def record(self, op_version: str, execution: OperationExecution) -> None:
        record = HistoryRecord(execution_id=execution.execution_id, operation_id=execution.operation_id, version=op_version, status=execution.status, started_at=execution.started_at, completed_at=execution.completed_at, error=execution.error)
        self._records.append(record)

    def get(self, op_id: str) -> tuple[HistoryRecord, ...]:
        return tuple(r for r in self._records if r.operation_id == op_id)

    @property
    def all(self) -> tuple[HistoryRecord, ...]:
        return tuple(self._records)

    @property
    def count(self) -> int:
        return len(self._records)
