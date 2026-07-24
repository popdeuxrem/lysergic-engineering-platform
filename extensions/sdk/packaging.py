from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from extensions.sdk.manifest import ExtensionManifest


@dataclass
class ExtensionPackage:
    manifest: ExtensionManifest
    source_path: str = ""
    checksum: str = ""
    integrity_verified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class PackageInstaller:
    def __init__(self) -> None:
        self._packages: dict[str, ExtensionPackage] = {}

    def install(self, pkg: ExtensionPackage) -> None:
        self._packages[pkg.manifest.extension_id] = pkg

    def get(self, extension_id: str) -> ExtensionPackage | None:
        return self._packages.get(extension_id)

    def remove(self, extension_id: str) -> bool:
        if extension_id in self._packages:
            del self._packages[extension_id]
            return True
        return False

    @property
    def packages(self) -> dict[str, ExtensionPackage]:
        return dict(self._packages)

    @property
    def count(self) -> int:
        return len(self._packages)
