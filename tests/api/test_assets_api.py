from runtime.api.assets import AssetsAPI
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceRegistry
from runtime.services.resolver import DependencyResolver


def _make_manager() -> ServiceManager:
    return ServiceManager(
        registry=ServiceRegistry(),
        resolver=DependencyResolver(),
        lifecycle=LifecycleManager(),
        health=HealthService(),
        event_bus=EventBus(),
    )


def test_asset_store_and_get() -> None:
    api = AssetsAPI(_make_manager())
    asset = api.store("ast-1", "schema", version="0.1.0", description="Test schema")
    assert asset.asset_id == "ast-1"
    assert asset.asset_type == "schema"
    assert api.get("ast-1") is asset


def test_asset_get_missing() -> None:
    api = AssetsAPI(_make_manager())
    assert api.get("nonexistent") is None


def test_asset_list_all() -> None:
    api = AssetsAPI(_make_manager())
    api.store("a", "type-1")
    api.store("b", "type-2")
    assert len(api.list()) == 2


def test_asset_list_by_type() -> None:
    api = AssetsAPI(_make_manager())
    api.store("a", "schema")
    api.store("b", "schema")
    api.store("c", "template")
    assert len(api.list(asset_type="schema")) == 2
    assert len(api.list(asset_type="template")) == 1


def test_asset_remove() -> None:
    api = AssetsAPI(_make_manager())
    api.store("x", "test")
    assert api.remove("x") is True
    assert api.count() == 0


def test_asset_remove_missing() -> None:
    api = AssetsAPI(_make_manager())
    assert api.remove("nonexistent") is False


def test_asset_count_all() -> None:
    api = AssetsAPI(_make_manager())
    api.store("a", "schema")
    api.store("b", "template")
    assert api.count() == 2


def test_asset_count_by_type() -> None:
    api = AssetsAPI(_make_manager())
    api.store("a", "schema")
    api.store("b", "schema")
    api.store("c", "template")
    assert api.count(asset_type="schema") == 2
    assert api.count(asset_type="template") == 1


def test_asset_tag() -> None:
    api = AssetsAPI(_make_manager())
    api.store("x", "test")
    assert api.tag("x", ("important", "schema")) is True
    asset = api.get("x")
    assert asset is not None
    assert "important" in asset.tags
    assert "schema" in asset.tags


def test_asset_tag_missing() -> None:
    api = AssetsAPI(_make_manager())
    assert api.tag("nonexistent", ("tag",)) is False


def test_asset_shutdown_clears() -> None:
    api = AssetsAPI(_make_manager())
    api.store("a", "test")
    api.shutdown()
    assert api.count() == 0
