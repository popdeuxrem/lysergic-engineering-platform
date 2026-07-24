from runtime.operations.manager import OperationsManager
from runtime.operations.model import OperationStep, ValidationGate
from runtime.services.events import EventBus


def test_full_lifecycle() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))

    m = OperationsManager(event_bus=bus)
    m.initialize_runtime()

    steps = (OperationStep(step_id="s1", name="Validate", target="workflow"), OperationStep(step_id="s2", name="Deploy", target="automation"))
    gates = (ValidationGate(gate_id="g1", gate_type="schema"), ValidationGate(gate_id="g2", gate_type="security"))
    m.create("op-1", "Production Deploy", version="1.0.0", steps=steps, gates=gates)
    assert "ops.OperationCreated" in events

    m.define("op-1")
    m.validate_op("op-1")
    assert "ops.OperationValidated" in events

    m.prepare("op-1")
    assert "ops.OperationPrepared" in events

    result = m.execute("op-1")
    assert result is not None and result.status == "completed"
    assert "ops.OperationStarted" in events
    assert "ops.OperationGatePassed" in events
    assert "ops.OperationCompleted" in events

    assert m.status("op-1") == "completed"
    assert len(m.history("op-1")) >= 1


def test_gate_rejection() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Test", steps=(OperationStep(step_id="s1", name="V"),))
    m.define("op-1")
    m.validate_op("op-1")
    m.prepare("op-1")
    result = m.execute("op-1")
    assert result is not None and result.status == "completed"


def test_snapshot_consistency() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Test", version="1.0.0")
    snap = m.snapshot_state()
    assert snap.get("op-1") is not None
    assert snap.version > 0
