from __future__ import annotations

from extensions.sdk.compatibility import CompatibilityChecker
from extensions.sdk.manifest import ExtensionManifest
from runtime.extensions.exceptions import ManifestValidationError


class ExtensionRuntimeValidator:
    def __init__(self) -> None:
        self._compatibility = CompatibilityChecker()

    def validate_manifest(self, manifest: ExtensionManifest) -> None:
        errors: list[str] = []
        if not manifest.extension_id:
            errors.append("extension_id is required")
        if not manifest.name:
            errors.append("name is required")
        if not manifest.version:
            errors.append("version is required")
        compat, compat_msg = self._compatibility.check_sdk_compatibility(manifest.min_sdk_version)
        if not compat:
            errors.append(compat_msg)
        if errors:
            raise ManifestValidationError(manifest.extension_id, tuple(errors))

    def validate_dependencies(self, manifest: ExtensionManifest, available_ids: set[str]) -> None:
        errors: list[str] = []
        for dep in manifest.dependencies:
            if dep not in available_ids:
                errors.append(f"Unresolved dependency: {dep}")
        if errors:
            raise ManifestValidationError(manifest.extension_id, tuple(errors))
