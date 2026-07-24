from runtime.services.events import EventBus
from runtime.workflows.manager import WorkflowManager
from runtime.workflows.model import WorkflowDefinition, WorkflowStep


def test_full_lifecycle() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))

    m = WorkflowManager(event_bus=bus)
    m.initialize()

    steps = (WorkflowStep(step_id="s1", name="Validate"), WorkflowStep(step_id="s2", name="Deploy"))
    w = WorkflowDefinition(workflow_id="wf-1", name="Deploy Pipeline", version="1.0.0", steps=steps)
    m.create(w)
    assert "workflow.WorkflowCreated" in events

    m.validate("wf-1")
    assert "workflow.WorkflowValidated" in events
    state = m.lifecycle.state_of("wf-1")
    assert state is not None and state.value == "validated"

    result = m.execute("wf-1")
    assert "workflow.WorkflowStarted" in events
    assert "workflow.WorkflowCompleted" in events
    assert result is not None and result.status == "completed"
    assert len(result.step_results) == 2

    hist = m.get_history("wf-1")
    assert len(hist) == 1


def test_failed_validation() -> None:
    m = WorkflowManager()
    m.initialize()
    w = WorkflowDefinition(workflow_id="wf-1", name="", version="1.0.0", steps=(WorkflowStep(step_id="s1", name="S1"),))
    m.create(w)
    m.validate("wf-1")
    state = m.lifecycle.state_of("wf-1")
    assert state is not None and state.value == "failed"


def test_snapshot_consistency() -> None:
    m = WorkflowManager()
    m.initialize()
    m.create(WorkflowDefinition(workflow_id="wf-1", name="Test", version="1.0.0"))
    snap = m.snapshot_state()
    assert snap.get("wf-1") is not None
    assert snap.version > 0
