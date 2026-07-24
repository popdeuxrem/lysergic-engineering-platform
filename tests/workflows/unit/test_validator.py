from runtime.workflows.model import WorkflowDefinition, WorkflowStep
from runtime.workflows.validator import WorkflowValidator


def test_validate_valid() -> None:
    v = WorkflowValidator()
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0", steps=(WorkflowStep(step_id="s1", name="S1"),))
    result = v.validate_tier1(w)
    assert result.valid is True


def test_validate_missing_id() -> None:
    v = WorkflowValidator()
    w = WorkflowDefinition(workflow_id="", name="Test", version="1.0.0", steps=(WorkflowStep(step_id="s1", name="S1"),))
    result = v.validate_tier1(w)
    assert result.valid is False


def test_validate_missing_name() -> None:
    v = WorkflowValidator()
    w = WorkflowDefinition(workflow_id="wf-1", name="", version="1.0.0", steps=(WorkflowStep(step_id="s1", name="S1"),))
    result = v.validate_tier1(w)
    assert result.valid is False


def test_validate_no_steps() -> None:
    v = WorkflowValidator()
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0")
    result = v.validate_tier1(w)
    assert result.valid is False


def test_validate_duplicate_step_ids() -> None:
    v = WorkflowValidator()
    steps = (WorkflowStep(step_id="s1", name="S1"), WorkflowStep(step_id="s1", name="S1 dup"))
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0", steps=steps)
    result = v.validate_tier2(w)
    assert result.valid is False


def test_validate_tier2_no_duplicates() -> None:
    v = WorkflowValidator()
    steps = (WorkflowStep(step_id="s1", name="S1"), WorkflowStep(step_id="s2", name="S2"))
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0", steps=steps)
    result = v.validate_tier2(w)
    assert result.valid is True
