from runtime.workflows.exceptions import (
    ExecutionError,
    InvalidTransitionError,
    WorkflowNotFoundError,
)


def test_workflow_not_found() -> None:
    e = WorkflowNotFoundError("wf-1")
    assert e.workflow_id == "wf-1"
    assert "wf-1" in str(e)


def test_invalid_transition() -> None:
    e = InvalidTransitionError("created", "running")
    assert e.current == "created"
    assert e.target == "running"


def test_execution_error() -> None:
    e = ExecutionError("wf-1", "step-1", "failed")
    assert e.workflow_id == "wf-1"
    assert e.step == "step-1"
