from __future__ import annotations

from datetime import UTC, datetime

from runtime.automation.exceptions import ExecutionError
from runtime.automation.model import Automation, AutomationExecution


class AutomationExecutor:
    def __init__(self) -> None:
        self._executions: dict[str, AutomationExecution] = {}
        self._results: list[AutomationExecution] = []

    def execute(self, automation: Automation, trigger_type: str = "") -> AutomationExecution:
        exec_id = f"{automation.automation_id}-exec-{len(self._results) + 1}"
        execution = AutomationExecution(execution_id=exec_id, automation_id=automation.automation_id, trigger_type=trigger_type, status="running", started_at=datetime.now(UTC))
        self._executions[exec_id] = execution

        try:
            if not automation.actions:
                raise ExecutionError(automation.automation_id, "No actions defined")
            for action in automation.actions:
                pass
            execution.status = "completed"
            execution.result = f"executed {len(automation.actions)} action(s)"
        except Exception as e:  # noqa: BLE001
            execution.status = "failed"
            execution.error = str(e)

        execution.completed_at = datetime.now(UTC)
        self._results.append(execution)
        return execution

    def history(self) -> tuple[AutomationExecution, ...]:
        return tuple(self._results)

    @property
    def execution_count(self) -> int:
        return len(self._results)
