from src.application.audit.execution_audit import ExecutionAuditProjection
from src.domain.execution import Execution
from src.domain.execution_status import ExecutionStatus
from src.domain.repository import ExecutionRepository


class ExecutionAuditHandler:
    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository

    def audit_by_id(self, execution_id: str) -> ExecutionAuditProjection | None:
        execution = self._repository.get_by_id(execution_id)
        if execution is None:
            return None
        return self._audit(execution)

    def _audit(self, execution: Execution) -> ExecutionAuditProjection:
        issues: list[str] = []

        if execution.created_at > execution.updated_at:
            issues.append("created_at is after updated_at")

        if execution.status not in list(ExecutionStatus):
            issues.append(f"unknown status: {execution.status}")

        if execution.created_at is None:
            issues.append("created_at is missing")

        if execution.updated_at is None:
            issues.append("updated_at is missing")

        return ExecutionAuditProjection(
            execution_id=execution.execution_id,
            status=execution.status,
            valid=len(issues) == 0,
            issues=issues,
        )
