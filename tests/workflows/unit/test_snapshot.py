from runtime.workflows.model import WorkflowDefinition
from runtime.workflows.snapshot import WorkflowSnapshot


def test_snapshot_creation() -> None:
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0")
    snap = WorkflowSnapshot(definitions={"wf-1": w}, version=1)
    assert snap.count() == 1
    assert snap.get("wf-1") is w


def test_snapshot_list() -> None:
    definitions = {
        "a": WorkflowDefinition(workflow_id="a", name="A", version="1.0.0"),
        "b": WorkflowDefinition(workflow_id="b", name="B", version="2.0.0"),
    }
    snap = WorkflowSnapshot(definitions=definitions, version=1)
    assert len(snap.list()) == 2


def test_snapshot_version() -> None:
    snap = WorkflowSnapshot(definitions={}, version=5)
    assert snap.version == 5


def test_snapshot_to_dict() -> None:
    snap = WorkflowSnapshot(definitions={}, version=1)
    d = snap.to_dict()
    assert d["version"] == 1
    assert "timestamp" in d
