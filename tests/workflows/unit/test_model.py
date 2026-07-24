from runtime.workflows.model import (
    StepType,
    WorkflowDefinition,
    WorkflowResult,
    WorkflowStep,
)


def test_workflow_definition() -> None:
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0")
    assert w.workflow_id == "wf-1"
    assert w.step_count() == 0


def test_workflow_with_steps() -> None:
    steps = (WorkflowStep(step_id="s1", name="Step 1"), WorkflowStep(step_id="s2", name="Step 2"))
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", steps=steps)
    assert w.step_count() == 2
    assert w.step_ids() == ("s1", "s2")


def test_workflow_step_types() -> None:
    s = WorkflowStep(step_id="s1", name="Task", step_type=StepType.TASK)
    assert s.step_type == StepType.TASK


def test_workflow_result_successful() -> None:
    r = WorkflowResult(execution_id="e1", workflow_id="wf-1", status="completed")
    assert r.successful() is True
    assert r.failed() is False


def test_workflow_result_failed() -> None:
    r = WorkflowResult(execution_id="e1", workflow_id="wf-1", status="failed", error="fail")
    assert r.failed() is True
    assert r.successful() is False
