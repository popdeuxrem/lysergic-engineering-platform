from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from extensions.sdk.extension import Extension, ExtensionHealth
from extensions.sdk.manifest import ExtensionManifest


class ExtensionState(Enum):
    DISCOVERED = "discovered"
    VALIDATED = "validated"
    LOADING = "loading"
    READY = "ready"
    FAILED = "failed"
    STOPPED = "stopped"
    REMOVED = "removed"


@dataclass
class ExtensionStateRecord:
    extension_id: str
    state: ExtensionState = ExtensionState.DISCOVERED
    manifest: ExtensionManifest | None = None
    extension: Extension | None = None
    health: ExtensionHealth = ExtensionHealth.UNKNOWN
    loaded_at: datetime | None = None
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class ExtensionRegistry:
    def __init__(self) -> None:
        self._records: dict[str, ExtensionStateRecord] = {}

    def store(self, manifest: ExtensionManifest) -> ExtensionStateRecord:
        record = ExtensionStateRecord(
            extension_id=manifest.extension_id,
            manifest=manifest,
        )
        self._records[manifest.extension_id] = record
        return record

    def get(self, extension_id: str) -> ExtensionState | None:
        record = self._records.get(extension_id)
        return record.state if record else None

    def manifest(self, extension_id: str) -> ExtensionManifest | None:
        record = self._records.get(extension_id)
        return record.manifest if record else None

    def get_extension(self, extension_id: str) -> Extension | None:
        record = self._records.get(extension_id)
        return record.extension if record else None

    def set_extension(self, extension_id: str, extension: Extension) -> None:
        record = self._records.get(extension_id)
        if record is not None:
            record.extension = extension
            record.loaded_at = datetime.now(UTC)

    def set_state(self, extension_id: str, state: ExtensionState) -> None:
        record = self._records.get(extension_id)
        if record is not None:
            record.state = state

    def set_health(self, extension_id: str, health: ExtensionHealth) -> None:
        record = self._records.get(extension_id)
        if record is not None:
            record.health = health

    def remove(self, extension_id: str) -> bool:
        if extension_id in self._records:
            del self._records[extension_id]
            return True
        return False

    def list_by_state(self, state: ExtensionState) -> tuple[ExtensionStateRecord, ...]:
        return tuple(r for r in self._records.values() if r.state == state)

    @property
    def installed(self) -> tuple[ExtensionStateRecord, ...]:
        return tuple(self._records.values())

    @property
    def ready(self) -> tuple[ExtensionStateRecord, ...]:
        return tuple(r for r in self._records.values() if r.state == ExtensionState.READY)

    @property
    def failed(self) -> tuple[ExtensionStateRecord, ...]:
        return tuple(r for r in self._records.values() if r.state == ExtensionState.FAILED)

    @property
    def count(self) -> int:
        return len(self._records)

    def __contains__(self, extension_id: str) -> bool:
        return extension_id in self._records

    def __len__(self) -> int:
        return len(self._records)
