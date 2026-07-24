from runtime.api.extensions import ExtensionAPI, ExtensionState


def _make_api() -> ExtensionAPI:
    from runtime.kernel.lifecycle import LifecycleManager
    from runtime.services.events import EventBus
    from runtime.services.health import HealthService
    from runtime.services.manager import ServiceManager
    from runtime.services.registry import ServiceRegistry
    from runtime.services.resolver import DependencyResolver
    m = ServiceManager(registry=ServiceRegistry(), resolver=DependencyResolver(), lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus())
    return ExtensionAPI(m)


def test_list_empty() -> None:
    api = _make_api()
    assert api.list() == ()


def test_register() -> None:
    api = _make_api()
    record = api.register("ext-1", "Test", "1.0.0")
    assert record.extension_id == "ext-1"
    assert record.name == "Test"
    assert record.state == ExtensionState.DISCOVERED


def test_get() -> None:
    api = _make_api()
    api.register("ext-1", "Test", "1.0.0")
    assert api.get("ext-1") is not None
    assert api.get("missing") is None


def test_install() -> None:
    api = _make_api()
    api.register("ext-1", "Test", "1.0.0")
    result = api.install("ext-1", "/path/to/ext")
    assert result is not None
    assert result.state == ExtensionState.INSTALLED
    assert result.source == "/path/to/ext"


def test_install_missing() -> None:
    api = _make_api()
    assert api.install("missing", "/path") is None


def test_enable() -> None:
    api = _make_api()
    api.register("ext-1", "Test", "1.0.0")
    api.install("ext-1", "/path")
    result = api.enable("ext-1")
    assert result is not None
    assert result.state == ExtensionState.ENABLED
    assert api.is_enabled("ext-1") is True


def test_disable() -> None:
    api = _make_api()
    api.register("ext-1", "Test", "1.0.0")
    api.install("ext-1", "/path")
    api.enable("ext-1")
    result = api.disable("ext-1")
    assert result is not None
    assert result.state == ExtensionState.DISABLED
    assert api.is_enabled("ext-1") is False


def test_remove() -> None:
    api = _make_api()
    api.register("ext-1", "Test", "1.0.0")
    assert api.remove("ext-1") is True
    assert api.count() == 0


def test_remove_missing() -> None:
    api = _make_api()
    assert api.remove("missing") is False


def test_count() -> None:
    api = _make_api()
    assert api.count() == 0
    api.register("a", "A", "1.0.0")
    assert api.count() == 1


def test_list_by_state() -> None:
    api = _make_api()
    api.register("a", "A", "1.0.0")
    api.register("b", "B", "1.0.0")
    api.install("a", "/path")
    api.enable("a")
    assert len(api.list_by_state(ExtensionState.ENABLED)) == 1
    assert len(api.list_by_state(ExtensionState.DISCOVERED)) == 1


def test_shutdown_clears() -> None:
    api = _make_api()
    api.register("x", "X", "1.0.0")
    api.shutdown()
    assert api.count() == 0


def test_metadata() -> None:
    api = _make_api()
    m = api.metadata()
    assert m["count"] == 0
