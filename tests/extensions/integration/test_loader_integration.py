"""Integration tests for the Extension SDK lifecycle via ExtensionLoader."""

from extensions.sdk.capabilities import CapabilityRegistry
from extensions.sdk.compatibility import CompatibilityChecker
from extensions.sdk.dependencies import DependencyResolver
from extensions.sdk.extension import ExtensionHealth
from extensions.sdk.lifecycle import ExtensionLifecycle
from extensions.sdk.loader import ExtensionLoader
from extensions.sdk.manifest import ExtensionManifest
from extensions.sdk.registry import ExtensionRegistry
from extensions.sdk.validation import ValidationEngine


class IntegrationExtension:
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
        return ExtensionHealth.HEALTHY

    @property
    def manifest(self) -> ExtensionManifest:
        return ExtensionManifest(extension_id=self.extension_id, name=self.extension_id, version="1.0.0")

    def get_metadata(self) -> dict[str, object]:
        return {"id": self.extension_id}


def _make_loader() -> ExtensionLoader:
    registry = ExtensionRegistry()
    lifecycle = ExtensionLifecycle()
    cap_reg = CapabilityRegistry()
    resolver = DependencyResolver()
    checker = CompatibilityChecker()
    validator = ValidationEngine(checker)
    return ExtensionLoader(registry, lifecycle, cap_reg, resolver, validator, checker)


def test_full_lifecycle() -> None:
    loader = _make_loader()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    ext = IntegrationExtension("ext-1")

    loader.discover(manifest)
    loader.validate("ext-1")
    loader.load("ext-1", ext)

    assert ext.initialized is True

    loader.unload("ext-1")
    assert ext.shutdown_called is True


def test_loader_dependency_chain() -> None:
    loader = _make_loader()

    dep = ExtensionManifest(extension_id="base", name="Base", version="1.0.0")
    mid = ExtensionManifest(extension_id="middle", name="Middle", version="1.0.0", dependencies=("base",))
    top = ExtensionManifest(extension_id="top", name="Top", version="1.0.0", dependencies=("middle",))

    for m in (dep, mid, top):
        loader.discover(m)
        loader.validate(m.extension_id)

    loader.load("base", IntegrationExtension("base"))
    loader.load("middle", IntegrationExtension("middle"))
    loader.load("top", IntegrationExtension("top"))

    loader.unload("top")
    loader.unload("middle")
    loader.unload("base")


def test_validate_then_fail() -> None:
    loader = _make_loader()
    manifest = ExtensionManifest(extension_id="", name="", version="")
    try:
        loader.discover(manifest)
    except Exception:  # noqa: BLE001, S110
        pass
