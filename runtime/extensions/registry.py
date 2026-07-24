from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from extensions.sdk.manifest import ExtensionManifest
from runtime.extensions.exceptions import (
    ExtensionRuntimeConflictError,
    RegistryFrozenError,
)


@dataclass
class ExtensionRuntimeRecord:
    extension_id: str
    manifest: ExtensionManifest
    state: str = "installed"
    install_path: str = ""
    installed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    health: str = "unknown"
    error: str = ""


class ExtensionRuntimeRegistry:
    def __init__(self) -> None:
        self._records: dict[str, ExtensionRuntimeRecord] = {}
        self._frozen = False

    def register(self, record: ExtensionRuntimeRecord) -> None:
        if self._frozen:
            raise RegistryFrozenError()
        if record.extension_id in self._records:
            raise ExtensionRuntimeConflictError(record.extension_id)
        self._records[record.extension_id] = record

    def get(self, extension_id: str) -> ExtensionRuntimeRecord | None:
        return self._records.get(extension_id)

    def unregister(self, extension_id: str) -> bool:
        if self._frozen:
            raise RegistryFrozenError()
        return self._records.pop(extension_id, None) is not None

    def list(self) -> tuple[ExtensionRuntimeRecord, ...]:
        return tuple(self._records.values())

    def list_by_state(self, state: str) -> tuple[ExtensionRuntimeRecord, ...]:
        return tuple(r for r in self._records.values() if r.state == state)

    def set_state(self, extension_id: str, state: str) -> None:
        record = self._records.get(extension_id)
        if record is not None:
            record.state = state

    def set_error(self, extension_id: str, error: str) -> None:
        record = self._records.get(extension_id)
        if record is not None:
            record.error = error

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def count(self) -> int:
        return len(self._records)

    def __contains__(self, extension_id: str) -> bool:
        return extension_id in self._records
