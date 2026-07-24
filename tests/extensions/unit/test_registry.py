from extensions.sdk.extension import ExtensionHealth
from extensions.sdk.manifest import ExtensionManifest
from extensions.sdk.registry import ExtensionRegistry, ExtensionState


class FakeExtension:
    def __init__(self, eid: str) -> None:
        self.extension_id = eid
    def initialize(self) -> None: ...
    def shutdown(self) -> None: ...
    @property
    def health(self) -> ExtensionHealth:
        return ExtensionHealth.HEALTHY
    @property
    def manifest(self) -> ExtensionManifest:
        return ExtensionManifest(extension_id=self.extension_id, name=self.extension_id, version="1.0.0")
    def get_metadata(self) -> dict[str, object]:
        return {}


def test_registry_store_and_get() -> None:
    r = ExtensionRegistry()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    r.store(manifest)
    assert r.get("ext-1") == ExtensionState.DISCOVERED
    assert "ext-1" in r


def test_registry_manifest() -> None:
    r = ExtensionRegistry()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    r.store(manifest)
    assert r.manifest("ext-1") is manifest


def test_registry_set_state() -> None:
    r = ExtensionRegistry()
    r.store(ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0"))
    r.set_state("ext-1", ExtensionState.READY)
    assert r.get("ext-1") == ExtensionState.READY


def test_registry_set_extension() -> None:
    r = ExtensionRegistry()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    r.store(manifest)
    ext = FakeExtension("ext-1")
    r.set_extension("ext-1", ext)
    assert r.get_extension("ext-1") is ext


def test_registry_set_health() -> None:
    r = ExtensionRegistry()
    r.store(ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0"))
    r.set_health("ext-1", ExtensionHealth.DEGRADED)
    record = r.installed[0]
    assert record.health == ExtensionHealth.DEGRADED


def test_registry_remove() -> None:
    r = ExtensionRegistry()
    r.store(ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0"))
    assert r.remove("ext-1") is True
    assert "ext-1" not in r


def test_registry_remove_missing() -> None:
    r = ExtensionRegistry()
    assert r.remove("nonexistent") is False


def test_registry_list_by_state() -> None:
    r = ExtensionRegistry()
    r.store(ExtensionManifest(extension_id="a", name="A", version="1.0.0"))
    r.store(ExtensionManifest(extension_id="b", name="B", version="1.0.0"))
    r.set_state("a", ExtensionState.READY)
    ready = r.list_by_state(ExtensionState.READY)
    assert len(ready) == 1
    assert ready[0].extension_id == "a"


def test_registry_properties() -> None:
    r = ExtensionRegistry()
    r.store(ExtensionManifest(extension_id="a", name="A", version="1.0.0"))
    r.store(ExtensionManifest(extension_id="b", name="B", version="1.0.0"))
    r.set_state("a", ExtensionState.READY)
    assert len(r.installed) == 2
    assert len(r.ready) == 1
    assert r.count == 2
