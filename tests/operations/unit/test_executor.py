from runtime.operations.executor import OperationsExecutor
from runtime.operations.model import EngineeringOperation, OperationStep


def test_execute() -> None:
    ex = OperationsExecutor()
    steps = (OperationStep(step_id="s1", name="Validate"),)
    o = EngineeringOperation(operation_id="op-1", name="Test", version="1.0.0", steps=steps)
    result = ex.execute(o)
    assert result.status == "completed"
    assert ex.execution_count == 1


def test_execute_no_steps() -> None:
    ex = OperationsExecutor()
    o = EngineeringOperation(operation_id="op-1", name="Test", version="1.0.0")
    result = ex.execute(o)
    assert result.status == "completed"
