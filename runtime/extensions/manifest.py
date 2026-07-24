from __future__ import annotations

from pathlib import Path

from extensions.sdk.compatibility import CompatibilityChecker
from extensions.sdk.manifest import ExtensionManifest
from extensions.sdk.validation import ValidationEngine


class ExtensionManifestLoader:
    def __init__(self) -> None:
        self._compatibility = CompatibilityChecker()
        self._validator = ValidationEngine(self._compatibility)

    def load(self, path: str | Path) -> ExtensionManifest:
        path = Path(path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Manifest not found: {path}")
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        manifest = ExtensionManifest(
            extension_id=data.get("extension_id", ""),
            name=data.get("name", ""),
            version=data.get("version", ""),
            description=data.get("description", ""),
            author=data.get("author", ""),
            dependencies=tuple(data.get("dependencies", [])),
            capabilities=tuple(data.get("capabilities", [])),
            entry_point=data.get("entry_point", ""),
        )
        self._validator.validate_manifest(manifest)
        return manifest
