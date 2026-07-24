from runtime.operations.model import EngineeringOperation
from runtime.operations.registry import OperationsRegistry


def test_register() -> None:
    r = OperationsRegistry()
    r.register(EngineeringOperation(operation_id="op-1", name="Test", version="1.0.0"))
    assert "op-1" in r
    assert r.count == 1


def test_duplicate_raises() -> None:
    r = OperationsRegistry()
    r.register(EngineeringOperation(operation_id="op-1", name="T", version="1.0.0"))
    try:
        r.register(EngineeringOperation(operation_id="op-1", name="T", version="1.0.0"))
        assert False
    except Exception:
        pass


def test_get() -> None:
    r = OperationsRegistry()
    o = EngineeringOperation(operation_id="op-1", name="T", version="1.0.0")
    r.register(o)
    assert r.get("op-1") is o
    assert r.get("missing") is None


def test_unregister() -> None:
    r = OperationsRegistry()
    r.register(EngineeringOperation(operation_id="a", name="A", version="1.0.0"))
    assert r.unregister("a") is True
    assert r.count == 0


def test_list() -> None:
    r = OperationsRegistry()
    r.register(EngineeringOperation(operation_id="a", name="A", version="1.0.0"))
    r.register(EngineeringOperation(operation_id="b", name="B", version="2.0.0"))
    assert len(r.list()) == 2


def test_freeze() -> None:
    r = OperationsRegistry()
    r.freeze()
    try:
        r.register(EngineeringOperation(operation_id="late", name="Late", version="1.0.0"))
        assert False
    except Exception:
        pass
