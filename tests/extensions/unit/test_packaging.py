from extensions.sdk.manifest import ExtensionManifest
from extensions.sdk.packaging import ExtensionPackage, PackageInstaller


def test_package_creation() -> None:
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    pkg = ExtensionPackage(manifest=manifest, source_path="/tmp/ext-1")
    assert pkg.manifest.extension_id == "ext-1"
    assert pkg.source_path == "/tmp/ext-1"


def test_installer_install_and_get() -> None:
    installer = PackageInstaller()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    pkg = ExtensionPackage(manifest=manifest)
    installer.install(pkg)
    retrieved = installer.get("ext-1")
    assert retrieved is not None
    assert retrieved.manifest.extension_id == "ext-1"


def test_installer_get_missing() -> None:
    installer = PackageInstaller()
    assert installer.get("nonexistent") is None


def test_installer_remove() -> None:
    installer = PackageInstaller()
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    installer.install(ExtensionPackage(manifest=manifest))
    assert installer.remove("ext-1") is True
    assert installer.count == 0


def test_installer_remove_missing() -> None:
    installer = PackageInstaller()
    assert installer.remove("nonexistent") is False


def test_installer_packages_property() -> None:
    installer = PackageInstaller()
    manifest = ExtensionManifest(extension_id="e1", name="E1", version="1.0.0")
    installer.install(ExtensionPackage(manifest=manifest))
    assert "e1" in installer.packages
