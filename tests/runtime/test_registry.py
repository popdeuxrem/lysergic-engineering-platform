
from runtime.kernel.registry import ComponentRegistry


class FakeComponent:
    def __init__(self, cid: str) -> None:
        self.component_id = cid
        self.initialized = False
        self.shutdown_called = False

    def initialize(self) -> None:
        self.initialized = True

    def shutdown(self) -> None:
        self.shutdown_called = True


def test_register_and_resolve() -> None:
    registry: ComponentRegistry[FakeComponent] = ComponentRegistry()
    comp = FakeComponent("test")
    registry.register(comp)
    assert registry.resolve("test") is comp


def test_register_duplicate_raises() -> None:
    registry: ComponentRegistry[FakeComponent] = ComponentRegistry()
    registry.register(FakeComponent("dup"))
    try:
        registry.register(FakeComponent("dup"))
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_freeze_prevents_registration() -> None:
    registry: ComponentRegistry[FakeComponent] = ComponentRegistry()
    registry.freeze()
    try:
        registry.register(FakeComponent("late"))
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass


def test_initialize_all_calls_all_components() -> None:
    registry: ComponentRegistry[FakeComponent] = ComponentRegistry()
    a = FakeComponent("a")
    b = FakeComponent("b")
    registry.register(a)
    registry.register(b)
    registry.initialize_all()

    assert a.initialized is True
    assert b.initialized is True
    assert registry.frozen is True


def test_shutdown_all_reverses_order() -> None:
    registry: ComponentRegistry[FakeComponent] = ComponentRegistry()
    a = FakeComponent("a")
    b = FakeComponent("b")
    registry.register(a)
    registry.register(b)
    registry.initialize_all()
    registry.shutdown_all()

    assert a.shutdown_called is True
    assert b.shutdown_called is True


def test_initialization_order() -> None:
    registry: ComponentRegistry[FakeComponent] = ComponentRegistry()
    registry.register(FakeComponent("first"))
    registry.register(FakeComponent("second"))
    assert registry.initialization_order == ["first", "second"]


def test_contains() -> None:
    registry: ComponentRegistry[FakeComponent] = ComponentRegistry()
    registry.register(FakeComponent("x"))
    assert "x" in registry
    assert "y" not in registry


def test_len() -> None:
    registry: ComponentRegistry[FakeComponent] = ComponentRegistry()
    assert len(registry) == 0
    registry.register(FakeComponent("a"))
    assert len(registry) == 1
