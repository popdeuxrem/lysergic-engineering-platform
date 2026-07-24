from runtime.api.extensions import ExtensionAPI, ExtensionManifest
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


def test_extension_list_empty() -> None:
    api = ExtensionAPI(_make_manager())
    assert api.list() == ()


def test_extension_register_and_list() -> None:
    api = ExtensionAPI(_make_manager())
    manifest = ExtensionManifest(extension_id="ext-1", name="Test Extension", version="1.0.0")
    api.register(manifest)
    assert len(api.list()) == 1
    assert api.list()[0].extension_id == "ext-1"


def test_extension_get() -> None:
    api = ExtensionAPI(_make_manager())
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    api.register(manifest)
    result = api.get("ext-1")
    assert result is not None
    assert result.name == "Test"


def test_extension_get_missing() -> None:
    api = ExtensionAPI(_make_manager())
    assert api.get("nonexistent") is None


def test_extension_unregister() -> None:
    api = ExtensionAPI(_make_manager())
    api.register(ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0"))
    api.unregister("ext-1")
    assert api.count() == 0


def test_extension_count() -> None:
    api = ExtensionAPI(_make_manager())
    api.register(ExtensionManifest(extension_id="a", name="A", version="1.0.0"))
    api.register(ExtensionManifest(extension_id="b", name="B", version="2.0.0"))
    assert api.count() == 2


def test_extension_shutdown_clears() -> None:
    api = ExtensionAPI(_make_manager())
    api.register(ExtensionManifest(extension_id="x", name="X", version="1.0.0"))
    api.shutdown()
    assert api.count() == 0
