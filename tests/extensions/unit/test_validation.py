from extensions.sdk.compatibility import CompatibilityChecker
from extensions.sdk.manifest import ExtensionManifest
from extensions.sdk.validation import ValidationEngine, ValidationTier


def test_validate_valid_manifest() -> None:
    v = ValidationEngine(CompatibilityChecker())
    manifest = ExtensionManifest(extension_id="ext-1", name="Test", version="1.0.0")
    result = v.validate_manifest(manifest)
    assert result.passed is True
    assert result.tier == ValidationTier.TIER_1


def test_validate_missing_extension_id() -> None:
    v = ValidationEngine(CompatibilityChecker())
    manifest = ExtensionManifest(extension_id="", name="Test", version="1.0.0")
    from extensions.sdk.manifest import ManifestValidationError
    try:
        v.validate_manifest(manifest)
        assert False, "Expected ManifestValidationError"
    except ManifestValidationError as exc:
        assert any("extension_id" in e for e in exc.errors)


def test_validate_missing_name() -> None:
    v = ValidationEngine(CompatibilityChecker())
    manifest = ExtensionManifest(extension_id="e", name="", version="1.0.0")
    try:
        v.validate_manifest(manifest)
        assert False, "Expected ManifestValidationError"
    except Exception:  # noqa: BLE001, S110
        pass


def test_validate_missing_version() -> None:
    v = ValidationEngine(CompatibilityChecker())
    manifest = ExtensionManifest(extension_id="e", name="E", version="")
    try:
        v.validate_manifest(manifest)
        assert False, "Expected ManifestValidationError"
    except Exception:  # noqa: BLE001, S110
        pass


def test_validate_manifest_sdk_warning() -> None:
    v = ValidationEngine(CompatibilityChecker())
    manifest = ExtensionManifest(extension_id="e", name="E", version="1.0.0", min_sdk_version="99.0.0")
    result = v.validate_manifest(manifest)
    assert result.passed is True
    assert len(result.warnings) > 0


def test_clear_results() -> None:
    v = ValidationEngine(CompatibilityChecker())
    manifest = ExtensionManifest(extension_id="e", name="E", version="1.0.0")
    v.validate_manifest(manifest)
    assert len(v.results) == 1
    v.clear()
    assert len(v.results) == 0
