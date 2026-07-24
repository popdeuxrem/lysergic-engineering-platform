from runtime.operations.model import (
    EngineeringOperation,
    OperationExecution,
    OperationStep,
    ValidationGate,
)


def test_operation_creation() -> None:
    o = EngineeringOperation(operation_id="op-1", name="Deploy", version="1.0.0")
    assert o.operation_id == "op-1"
    assert o.name == "Deploy"


def test_operation_with_steps() -> None:
    steps = (OperationStep(step_id="s1", name="Validate"), OperationStep(step_id="s2", name="Deploy"))
    o = EngineeringOperation(operation_id="op-1", name="Test", version="1.0.0", steps=steps)
    assert len(o.steps) == 2


def test_operation_with_gates() -> None:
    gates = (ValidationGate(gate_id="g1", gate_type="schema"), ValidationGate(gate_id="g2", gate_type="security"))
    o = EngineeringOperation(operation_id="op-1", name="Test", version="1.0.0", gates=gates)
    assert len(o.gates) == 2


def test_execution() -> None:
    e = OperationExecution(execution_id="e1", operation_id="op-1", status="completed")
    assert e.status == "completed"
