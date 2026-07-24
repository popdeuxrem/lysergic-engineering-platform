from __future__ import annotations

from datetime import UTC, datetime

from runtime.workflows.lifecycle import WorkflowLifecycle, WorkflowStatus
from runtime.workflows.model import (
    StepResult,
    WorkflowDefinition,
    WorkflowExecution,
    WorkflowResult,
    WorkflowStep,
)


class WorkflowExecutor:
    def __init__(self, lifecycle: WorkflowLifecycle) -> None:
        self._lifecycle = lifecycle
        self._executions: dict[str, WorkflowExecution] = {}
        self._results: list[WorkflowResult] = []

    def execute(self, definition: WorkflowDefinition) -> WorkflowResult:
        wf_id = definition.workflow_id
        exec_id = f"{wf_id}-exec-{len(self._executions) + 1}"
        step_results: list[StepResult] = []

        execution = WorkflowExecution(
            execution_id=exec_id, workflow_id=wf_id, status="running", started_at=datetime.now(UTC),
        )
        self._executions[exec_id] = execution

        self._lifecycle.transition(wf_id, WorkflowStatus.RUNNING)

        for step in definition.steps:
            sr = self._execute_step(exec_id, step)
            step_results.append(sr)
            if sr.status == "failed":
                self._lifecycle.transition(wf_id, WorkflowStatus.FAILED)
                result = WorkflowResult(
                    execution_id=exec_id, workflow_id=wf_id, status="failed",
                    started_at=execution.started_at, completed_at=datetime.now(UTC),
                    step_results=tuple(step_results), error=sr.error,
                )
                self._results.append(result)
                return result

        self._lifecycle.transition(wf_id, WorkflowStatus.COMPLETED)
        result = WorkflowResult(
            execution_id=exec_id, workflow_id=wf_id, status="completed",
            started_at=execution.started_at, completed_at=datetime.now(UTC),
            step_results=tuple(step_results),
        )
        self._results.append(result)
        return result

    def _execute_step(self, exec_id: str, step: WorkflowStep) -> StepResult:
        started = datetime.now(UTC)
        try:
            if step.step_type.value == "task":
                result = self._run_task(step)
            else:
                result = None
            return StepResult(step_id=step.step_id, status="completed", started_at=started, completed_at=datetime.now(UTC), output=result)
        except Exception as e:  # noqa: BLE001
            return StepResult(step_id=step.step_id, status="failed", started_at=started, completed_at=datetime.now(UTC), error=str(e))

    def _run_task(self, step: WorkflowStep) -> str:
        return f"step:{step.step_id} completed"

    def stop(self, workflow_id: str) -> WorkflowResult | None:
        for eid, exec_ in self._executions.items():
            if exec_.workflow_id == workflow_id and exec_.status == "running":
                self._lifecycle.transition(workflow_id, WorkflowStatus.STOPPED)
                result = WorkflowResult(
                    execution_id=eid, workflow_id=workflow_id, status="stopped",
                    started_at=exec_.started_at, completed_at=datetime.now(UTC),
                    step_results=exec_.step_results,
                )
                self._executions[eid] = WorkflowExecution(
                    execution_id=eid, workflow_id=workflow_id, status="stopped",
                    started_at=exec_.started_at, completed_at=datetime.now(UTC),
                )
                self._results.append(result)
                return result
        return None

    @property
    def results(self) -> tuple[WorkflowResult, ...]:
        return tuple(self._results)

    @property
    def execution_count(self) -> int:
        return len(self._executions)
