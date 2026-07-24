from runtime.workflows.model import WorkflowDefinition
from runtime.workflows.registry import WorkflowRegistry


def test_register() -> None:
    r = WorkflowRegistry()
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0")
    r.register(w)
    assert "wf-1" in r
    assert r.count == 1


def test_register_duplicate_raises() -> None:
    r = WorkflowRegistry()
    r.register(WorkflowDefinition(workflow_id="wf-1", name="T", version="1.0.0"))
    try:
        r.register(WorkflowDefinition(workflow_id="wf-1", name="T", version="1.0.0"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_get() -> None:
    r = WorkflowRegistry()
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0")
    r.register(w)
    assert r.get("wf-1") is w
    assert r.get("missing") is None


def test_unregister() -> None:
    r = WorkflowRegistry()
    r.register(WorkflowDefinition(workflow_id="a", name="A", version="1.0.0"))
    assert r.unregister("a") is True
    assert r.count == 0


def test_list() -> None:
    r = WorkflowRegistry()
    r.register(WorkflowDefinition(workflow_id="a", name="A", version="1.0.0"))
    r.register(WorkflowDefinition(workflow_id="b", name="B", version="2.0.0"))
    assert len(r.list()) == 2


def test_list_by_tag() -> None:
    r = WorkflowRegistry()
    r.register(WorkflowDefinition(workflow_id="a", name="A", version="1.0.0", tags=("core",)))
    r.register(WorkflowDefinition(workflow_id="b", name="B", version="1.0.0", tags=("test",)))
    assert len(r.list_by_tag("core")) == 1


def test_freeze() -> None:
    r = WorkflowRegistry()
    r.freeze()
    try:
        r.register(WorkflowDefinition(workflow_id="late", name="Late", version="1.0.0"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass
