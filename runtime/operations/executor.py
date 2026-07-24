from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.operations.model import (
    EngineeringOperation,
    OperationExecution,
    OperationStep,
)


class OperationsExecutor:
    def __init__(self) -> None:
        self._results: list[OperationExecution] = []

    def execute(self, op: EngineeringOperation) -> OperationExecution:
        exec_id = f"{op.operation_id}-exec-{len(self._results) + 1}"
        execution = OperationExecution(execution_id=exec_id, operation_id=op.operation_id, status="running", started_at=datetime.now(UTC))
        step_results: list[dict[str, Any]] = []

        try:
            for step in op.steps:
                sr = self._execute_step(step)
                step_results.append(sr)
                if sr.get("status") == "failed":
                    execution.status = "failed"
                    execution.error = sr.get("error", "Step failed")
                    break
            else:
                execution.status = "completed"

            execution.step_results = tuple(step_results)
        except Exception as e:
            execution.status = "failed"
            execution.error = str(e)

        execution.completed_at = datetime.now(UTC)
        self._results.append(execution)
        return execution

    def _execute_step(self, step: OperationStep) -> dict[str, Any]:
        return {"step_id": step.step_id, "status": "completed", "output": f"step:{step.step_id} executed"}

    @property
    def history(self) -> tuple[OperationExecution, ...]:
        return tuple(self._results)

    @property
    def execution_count(self) -> int:
        return len(self._results)
