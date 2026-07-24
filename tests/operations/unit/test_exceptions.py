from runtime.operations.exceptions import (
    GateRejectionError,
    InvalidLifecycleError,
    OperationNotFoundError,
)


def test_not_found() -> None:
    e = OperationNotFoundError("op-1")
    assert e.op_id == "op-1"


def test_invalid_lifecycle() -> None:
    e = InvalidLifecycleError("created", "executing")
    assert "created" in str(e)


def test_gate_rejection() -> None:
    e = GateRejectionError("op-1", "test", "tests failed")
    assert "test" in str(e)
