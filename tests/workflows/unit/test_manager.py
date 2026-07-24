from runtime.services.events import EventBus
from runtime.workflows.manager import WorkflowManager
from runtime.workflows.model import WorkflowDefinition, WorkflowStep


def test_initial_state() -> None:
    m = WorkflowManager()
    assert m.manager_status.name == "PENDING"


def test_initialize() -> None:
    m = WorkflowManager()
    m.initialize()
    assert m.manager_status.name == "READY"


def test_create() -> None:
    m = WorkflowManager()
    m.initialize()
    w = m.create(WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0"))
    assert w.workflow_id == "wf-1"
    assert m.get("wf-1") is not None


def test_get_missing() -> None:
    m = WorkflowManager()
    m.initialize()
    assert m.get("missing") is None


def test_list() -> None:
    m = WorkflowManager()
    m.initialize()
    m.create(WorkflowDefinition(workflow_id="a", name="A", version="1.0.0"))
    m.create(WorkflowDefinition(workflow_id="b", name="B", version="2.0.0"))
    assert len(m.list()) == 2


def test_validate() -> None:
    m = WorkflowManager()
    m.initialize()
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0", steps=(WorkflowStep(step_id="s1", name="S1"),))
    m.create(w)
    m.validate("wf-1")
    state = m.lifecycle.state_of("wf-1")
    assert state is not None and state.value == "validated"


def test_execute() -> None:
    m = WorkflowManager()
    m.initialize()
    steps = (WorkflowStep(step_id="s1", name="S1"), WorkflowStep(step_id="s2", name="S2"))
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0", steps=steps)
    m.create(w)
    result = m.execute("wf-1")
    assert result is not None
    assert result.status == "completed"


def test_execute_missing() -> None:
    m = WorkflowManager()
    m.initialize()
    assert m.execute("missing") is None


def test_status() -> None:
    m = WorkflowManager()
    m.initialize()
    m.create(WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0"))
    assert m.status("wf-1") == "created"
    assert m.status("missing") is None


def test_history() -> None:
    m = WorkflowManager()
    m.initialize()
    steps = (WorkflowStep(step_id="s1", name="S1"),)
    w = WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0", steps=steps)
    m.create(w)
    m.execute("wf-1")
    assert len(m.get_history("wf-1")) == 1


def test_snapshot() -> None:
    m = WorkflowManager()
    m.initialize()
    m.create(WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0"))
    snap = m.snapshot_state()
    assert snap.count() == 1


def test_events() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))
    m = WorkflowManager(event_bus=bus)
    m.initialize()
    m.create(WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0"))
    assert "workflow.WorkflowCreated" in events


def test_shutdown() -> None:
    m = WorkflowManager()
    m.initialize()
    m.create(WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0"))
    m.shutdown()
    assert m.get("wf-1") is None
