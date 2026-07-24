from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.extensions.registry import ExtensionRuntimeRecord


class ExtensionRuntimeSnapshot:
    def __init__(self, records: dict[str, ExtensionRuntimeRecord], version: int = 0) -> None:
        self._records = dict(records)
        self._version = version
        self._timestamp = datetime.now(UTC)

    def get(self, extension_id: str) -> ExtensionRuntimeRecord | None:
        return self._records.get(extension_id)

    def list(self) -> tuple[ExtensionRuntimeRecord, ...]:
        return tuple(self._records.values())

    def count(self) -> int:
        return len(self._records)

    @property
    def version(self) -> int:
        return self._version

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> dict[str, Any]:
        return {"version": self._version, "timestamp": self._timestamp.isoformat(), "extensions": [r.extension_id for r in self._records.values()]}
