from __future__ import annotations

from pathlib import Path

from extensions.sdk.manifest import ExtensionManifest


class FilesystemDiscovery:
    def __init__(self, base_paths: tuple[str, ...] = ("extensions",)) -> None:
        self._base_paths = [Path(p).resolve() for p in base_paths]

    def discover(self) -> tuple[ExtensionManifest, ...]:
        manifests: list[ExtensionManifest] = []
        for base in self._base_paths:
            if not base.exists():
                continue
            for path in base.iterdir():
                if path.is_dir():
                    manifest_path = path / "extension.yaml"
                    if manifest_path.exists():
                        import yaml
                        with open(manifest_path) as f:
                            data = yaml.safe_load(f) or {}
                        manifest = ExtensionManifest(
                            extension_id=data.get("extension_id", path.name),
                            name=data.get("name", path.name),
                            version=data.get("version", "0.1.0"),
                            description=data.get("description", ""),
                            author=data.get("author", ""),
                            dependencies=tuple(data.get("dependencies", [])),
                            capabilities=tuple(data.get("capabilities", [])),
                            entry_point=data.get("entry_point", ""),
                        )
                        manifests.append(manifest)
        return tuple(manifests)
