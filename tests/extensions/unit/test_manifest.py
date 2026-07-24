from extensions.sdk.manifest import ExtensionManifest, ExtensionPermission


def test_manifest_creation() -> None:
    manifest = ExtensionManifest(
        extension_id="ext-1",
        name="Test Extension",
        version="1.0.0",
        description="A test extension",
        author="test",
    )
    assert manifest.extension_id == "ext-1"
    assert manifest.version == "1.0.0"


def test_manifest_with_capabilities() -> None:
    manifest = ExtensionManifest(
        extension_id="ext-2",
        name="Capable",
        version="0.2.0",
        capabilities=("schema.validation", "graph.analysis"),
    )
    assert "schema.validation" in manifest.capabilities
    assert len(manifest.capabilities) == 2


def test_manifest_with_permissions() -> None:
    manifest = ExtensionManifest(
        extension_id="ext-3",
        name="Perms",
        version="1.0.0",
        permissions=(
            ExtensionPermission(resource="runtime.events", actions=("read", "write")),
            ExtensionPermission(resource="runtime.registry", actions=("read",)),
        ),
    )
    assert len(manifest.permissions) == 2
    assert manifest.permissions[0].resource == "runtime.events"


def test_manifest_with_dependencies() -> None:
    manifest = ExtensionManifest(
        extension_id="ext-4",
        name="Deps",
        version="1.0.0",
        dependencies=("dep-a", "dep-b"),
        optional_dependencies=("opt-dep",),
    )
    assert "dep-a" in manifest.dependencies
    assert "opt-dep" in manifest.optional_dependencies


def test_manifest_min_sdk() -> None:
    manifest = ExtensionManifest(extension_id="e", name="E", version="1.0.0", min_sdk_version="1.0.0")
    assert manifest.min_sdk_version == "1.0.0"


def test_manifest_defaults() -> None:
    manifest = ExtensionManifest(extension_id="e", name="E", version="1.0.0")
    assert manifest.dependencies == ()
    assert manifest.capabilities == ()
    assert manifest.permissions == ()
    assert manifest.min_sdk_version == "1.0.0"
    assert manifest.entry_point == ""
