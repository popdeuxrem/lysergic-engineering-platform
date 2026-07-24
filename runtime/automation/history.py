from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from runtime.automation.model import AutomationExecution


@dataclass
class HistoryRecord:
    execution_id: str
    automation_id: str
    trigger_type: str
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: str = ""
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id, "automation_id": self.automation_id,
            "trigger_type": self.trigger_type, "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result, "error": self.error,
        }


class AutomationHistory:
    def __init__(self) -> None:
        self._records: list[HistoryRecord] = []

    def record(self, execution: AutomationExecution) -> None:
        record = HistoryRecord(
            execution_id=execution.execution_id, automation_id=execution.automation_id,
            trigger_type=execution.trigger_type, status=execution.status,
            started_at=execution.started_at, completed_at=execution.completed_at,
            result=execution.result, error=execution.error,
        )
        self._records.append(record)

    def get(self, automation_id: str) -> tuple[HistoryRecord, ...]:
        return tuple(r for r in self._records if r.automation_id == automation_id)

    @property
    def all(self) -> tuple[HistoryRecord, ...]:
        return tuple(self._records)

    @property
    def count(self) -> int:
        return len(self._records)
