from extensions.sdk.capabilities import CapabilityRegistry
from extensions.sdk.compatibility import CompatibilityChecker
from extensions.sdk.dependencies import DependencyResolver
from extensions.sdk.extension import ExtensionHealth
from extensions.sdk.lifecycle import ExtensionLifecycle
from extensions.sdk.loader import ExtensionLoader
from extensions.sdk.manifest import ExtensionManifest
from extensions.sdk.registry import ExtensionRegistry
from extensions.sdk.validation import ValidationEngine


class FakeExtension:
    def __init__(self, eid: str) -> None:
        self.extension_id = eid
        self.initialized = False
        self.shutdown_called = False
    def initialize(self) -> None:
        self.initialized = True
    def shutdown(self) -> None:
        self.shutdown_called = True
    @property
    def health(self) -> ExtensionHealth:
        return ExtensionHealth.HEALTHY if self.initialized else ExtensionHealth.UNKNOWN
    @property
    def manifest(self) -> ExtensionManifest:
        return ExtensionManifest(extension_id=self.extension_id, name=self.extension_id, version="1.0.0")
    def get_metadata(self) -> dict[str, object]:
        return {}


def _make_loader() -> tuple[ExtensionLoader, ExtensionRegistry, ExtensionLifecycle]:
    registry = ExtensionRegistry()
    lifecycle = ExtensionLifecycle()
    cap_reg = CapabilityRegistry()
    resolver = DependencyResolver()
    checker = CompatibilityChecker()
    validator = ValidationEngine(checker)
    loader = ExtensionLoader(registry, lifecycle, cap_reg, resolver, validator, checker)
    return loader, registry, lifecycle


def test_discover_extension() -> None:
    loader, _registry, _ = _make_loader()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    state = loader.discover(manifest)
    assert state is not None


def test_validate_extension() -> None:
    loader, _, _lifecycle = _make_loader()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    loader.discover(manifest)
    state = loader.validate("ext-1")
    assert state is not None


def test_validate_invalid_manifest() -> None:
    loader, _, _ = _make_loader()
    manifest = ExtensionManifest(extension_id="", name="", version="")
    try:
        loader.discover(manifest)
        loader.validate("")
        assert False, "Expected failure on empty extension_id"
    except Exception:  # noqa: BLE001, S110
        pass


def test_load_extension() -> None:
    loader, _, _ = _make_loader()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    ext = FakeExtension("ext-1")
    loader.discover(manifest)
    loader.validate("ext-1")
    state = loader.load("ext-1", ext)
    assert state is not None
    assert ext.initialized is True


def test_load_extension_with_dependency() -> None:
    loader, _registry, _ = _make_loader()
    dep_manifest = ExtensionManifest(extension_id="dep-a", name="Dep A", version="1.0.0")
    main_manifest = ExtensionManifest(extension_id="main", name="Main", version="1.0.0", dependencies=("dep-a",))
    loader.discover(dep_manifest)
    loader.discover(main_manifest)
    loader.validate("dep-a")
    loader.validate("main")
    loader.load("dep-a", FakeExtension("dep-a"))
    state = loader.load("main", FakeExtension("main"))
    assert state is not None


def test_unload_extension() -> None:
    loader, _, _ = _make_loader()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    ext = FakeExtension("ext-1")
    loader.discover(manifest)
    loader.validate("ext-1")
    loader.load("ext-1", ext)
    state = loader.unload("ext-1")
    assert state is not None
    assert ext.shutdown_called is True


def test_remove_extension() -> None:
    loader, registry, _ = _make_loader()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    loader.discover(manifest)
    assert loader.remove("ext-1") is True
    assert "ext-1" not in registry


def test_remove_missing() -> None:
    loader, _, _ = _make_loader()
    assert loader.remove("nonexistent") is False
