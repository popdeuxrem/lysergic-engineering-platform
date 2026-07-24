from runtime.operations.manager import OperationsManager
from runtime.operations.model import OperationStep, ValidationGate
from runtime.services.events import EventBus


def test_initial_state() -> None:
    m = OperationsManager()
    assert m.manager_status.name == "PENDING"


def test_initialize() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    assert m.manager_status.name == "READY"


def test_create() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    o = m.create("op-1", "Deploy", version="1.0.0")
    assert o.operation_id == "op-1"
    assert m.get("op-1") is not None


def test_define() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Deploy")
    m.define("op-1")
    assert m.status("op-1") == "defined"


def test_validate() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Deploy", steps=(OperationStep(step_id="s1", name="Validate"),))
    m.define("op-1")
    m.validate_op("op-1")
    assert m.status("op-1") == "validated"


def test_prepare() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Deploy", steps=(OperationStep(step_id="s1", name="V"),))
    m.define("op-1")
    m.validate_op("op-1")
    m.prepare("op-1")
    assert m.status("op-1") == "ready"


def test_execute() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Deploy", steps=(OperationStep(step_id="s1", name="V"),))
    m.define("op-1")
    m.validate_op("op-1")
    m.prepare("op-1")
    result = m.execute("op-1")
    assert result is not None and result.status == "completed"


def test_execute_with_gates() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    gates = (ValidationGate(gate_id="g1", gate_type="schema"),)
    m.create("op-1", "Deploy", steps=(OperationStep(step_id="s1", name="V"),), gates=gates)
    m.define("op-1")
    m.validate_op("op-1")
    m.prepare("op-1")
    result = m.execute("op-1")
    assert result is not None and result.status == "completed"


def test_execute_missing() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    assert m.execute("missing") is None


def test_status() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Test")
    assert m.status("op-1") == "created"
    assert m.status("missing") is None


def test_list() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("a", "A")
    m.create("b", "B")
    assert len(m.list()) == 2


def test_history() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Deploy", steps=(OperationStep(step_id="s1", name="V"),))
    m.define("op-1")
    m.validate_op("op-1")
    m.prepare("op-1")
    m.execute("op-1")
    assert len(m.history("op-1")) >= 1


def test_archive() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Test")
    m.archive("op-1")
    assert m.status("op-1") == "archived"


def test_snapshot() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Test")
    snap = m.snapshot_state()
    assert snap.count() == 1


def test_events() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))
    m = OperationsManager(event_bus=bus)
    m.initialize_runtime()
    m.create("op-1", "Test")
    assert "ops.OperationCreated" in events


def test_shutdown() -> None:
    m = OperationsManager()
    m.initialize_runtime()
    m.create("op-1", "Test")
    m.shutdown()
    assert m.get("op-1") is None
