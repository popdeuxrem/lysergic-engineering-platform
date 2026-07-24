from runtime.api.assets import AssetsAPI


def _make_api() -> AssetsAPI:
    from runtime.kernel.lifecycle import LifecycleManager
    from runtime.services.events import EventBus
    from runtime.services.health import HealthService
    from runtime.services.manager import ServiceManager
    from runtime.services.registry import ServiceRegistry
    from runtime.services.resolver import DependencyResolver
    m = ServiceManager(registry=ServiceRegistry(), resolver=DependencyResolver(), lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus())
    return AssetsAPI(m)


def test_store_and_get() -> None:
    api = _make_api()
    a = api.store("ast-1", "schema", version="0.1.0")
    assert a.asset_id == "ast-1"
    assert api.get("ast-1") is a


def test_get_missing() -> None:
    api = _make_api()
    assert api.get("missing") is None


def test_list_all() -> None:
    api = _make_api()
    api.store("a", "schema")
    api.store("b", "template")
    assert len(api.list()) == 2


def test_list_by_type() -> None:
    api = _make_api()
    api.store("a", "schema")
    api.store("b", "schema")
    api.store("c", "template")
    assert len(api.list(asset_type="schema")) == 2
    assert len(api.list_by_type("schema")) == 2


def test_list_types() -> None:
    api = _make_api()
    api.store("a", "schema")
    api.store("b", "template")
    types = api.list_types()
    assert "schema" in types
    assert "template" in types


def test_search() -> None:
    api = _make_api()
    api.store("my-asset", "schema", description="important schema", tags=("core",))
    assert len(api.search("important")) == 1
    assert len(api.search("my-asset")) == 1
    assert len(api.search("core")) == 1
    assert len(api.search("x")) == 0


def test_remove() -> None:
    api = _make_api()
    api.store("x", "test")
    assert api.remove("x") is True
    assert api.count() == 0


def test_remove_missing() -> None:
    api = _make_api()
    assert api.remove("missing") is False


def test_count() -> None:
    api = _make_api()
    api.store("a", "schema")
    api.store("b", "template")
    assert api.count() == 2
    assert api.count(asset_type="schema") == 1


def test_tag() -> None:
    api = _make_api()
    api.store("x", "test")
    assert api.tag("x", ("important",)) is True
    a = api.get("x")
    assert a is not None and "important" in a.tags


def test_tag_missing() -> None:
    api = _make_api()
    assert api.tag("missing", ("t",)) is False


def test_shutdown_clears() -> None:
    api = _make_api()
    api.store("a", "test")
    api.shutdown()
    assert api.count() == 0
