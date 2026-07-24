from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExtensionPermission:
    resource: str
    actions: tuple[str, ...]


@dataclass(frozen=True)
class ExtensionManifest:
    extension_id: str
    name: str
    version: str
    description: str = ""
    author: str = ""
    dependencies: tuple[str, ...] = ()
    optional_dependencies: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    permissions: tuple[ExtensionPermission, ...] = ()
    min_sdk_version: str = "1.0.0"
    max_sdk_version: str | None = None
    entry_point: str = ""
    homepage: str = ""
    license: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class ManifestValidationError(Exception):
    def __init__(self, message: str, errors: tuple[str, ...] = ()) -> None:
        self.errors = errors
        super().__init__(message)
