from __future__ import annotations

from enum import Enum
from typing import Any, Protocol, runtime_checkable

from extensions.sdk.manifest import ExtensionManifest


class ExtensionHealth(Enum):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    STOPPED = "stopped"


@runtime_checkable
class Extension(Protocol):
    extension_id: str

    def initialize(self) -> None: ...

    def shutdown(self) -> None: ...

    @property
    def health(self) -> ExtensionHealth: ...

    @property
    def manifest(self) -> ExtensionManifest: ...

    def get_metadata(self) -> dict[str, Any]: ...
