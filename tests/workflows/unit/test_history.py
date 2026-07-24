from runtime.workflows.history import WorkflowHistory
from runtime.workflows.model import WorkflowResult


def test_record_and_get() -> None:
    h = WorkflowHistory()
    r = WorkflowResult(execution_id="e1", workflow_id="wf-1", status="completed")
    h.record(r)
    records = h.get("wf-1")
    assert len(records) == 1
    assert records[0].execution_id == "e1"


def test_get_execution() -> None:
    h = WorkflowHistory()
    h.record(WorkflowResult(execution_id="e1", workflow_id="wf-1", status="completed"))
    record = h.get_execution("e1")
    assert record is not None
    assert record.status == "completed"


def test_get_execution_missing() -> None:
    h = WorkflowHistory()
    assert h.get_execution("missing") is None


def test_all_records() -> None:
    h = WorkflowHistory()
    h.record(WorkflowResult(execution_id="e1", workflow_id="a", status="completed"))
    h.record(WorkflowResult(execution_id="e2", workflow_id="b", status="failed"))
    assert h.count == 2
