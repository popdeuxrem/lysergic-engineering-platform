from runtime.workflows.executor import WorkflowExecutor
from runtime.workflows.lifecycle import WorkflowLifecycle, WorkflowStatus
from runtime.workflows.model import WorkflowDefinition, WorkflowStep


def test_execute_success() -> None:
    lc = WorkflowLifecycle()
    ex = WorkflowExecutor(lc)
    steps = (WorkflowStep(step_id="s1", name="Step 1"), WorkflowStep(step_id="s2", name="Step 2"))
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0", steps=steps)
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.VALIDATED)
    lc.transition("wf-1", WorkflowStatus.READY)
    result = ex.execute(w)
    assert result is not None
    assert result.status == "completed"
    assert len(result.step_results) == 2


def test_execute_results() -> None:
    lc = WorkflowLifecycle()
    ex = WorkflowExecutor(lc)
    steps = (WorkflowStep(step_id="s1", name="S1"),)
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0", steps=steps)
    lc.initialize("wf-1")
    lc.transition("wf-1", WorkflowStatus.VALIDATED)
    lc.transition("wf-1", WorkflowStatus.READY)
    result = ex.execute(w)
    assert result is not None
    assert result.successful() is True


def test_executor_properties() -> None:
    lc = WorkflowLifecycle()
    ex = WorkflowExecutor(lc)
    assert ex.execution_count == 0
    assert ex.results == ()
