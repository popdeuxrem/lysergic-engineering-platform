from __future__ import annotations

from typing import Any

from runtime.operations.gates import GateResult
from runtime.operations.model import EngineeringOperation, OperationExecution


class OperationsReport:
    def __init__(self) -> None:
        self._reports: dict[str, dict[str, Any]] = {}

    def generate(self, op: EngineeringOperation, execution: OperationExecution, gate_results: tuple[GateResult, ...], artifacts: tuple[dict[str, Any], ...]) -> dict[str, Any]:
        report = {
            "operation_id": op.operation_id,
            "name": op.name,
            "version": op.version,
            "execution_id": execution.execution_id,
            "status": execution.status,
            "started_at": execution.started_at.isoformat() if execution.started_at else None,
            "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
            "steps": [{"step_id": s.step_id, "name": s.name} for s in op.steps],
            "gates": [{"gate_id": g.gate_id, "gate_type": g.gate_type, "outcome": g.outcome} for g in gate_results],
            "artifacts": list(artifacts),
            "error": execution.error,
        }
        self._reports[execution.execution_id] = report
        return report

    def get(self, execution_id: str) -> dict[str, Any] | None:
        return self._reports.get(execution_id)
