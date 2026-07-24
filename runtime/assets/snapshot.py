from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.assets.registry import AssetEntry


class AssetSnapshot:
    def __init__(self, entries: dict[str, AssetEntry], version: int = 0) -> None:
        self._entries = {k: v for k, v in entries.items()}
        self._version = version
        self._timestamp = datetime.now(UTC)

    def get(self, asset_id: str) -> AssetEntry | None:
        return self._entries.get(asset_id)

    def list(self) -> tuple[AssetEntry, ...]:
        return tuple(self._entries.values())

    def count(self) -> int:
        return len(self._entries)

    def version(self) -> int:
        return self._version

    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self._version,
            "timestamp": self._timestamp.isoformat(),
            "assets": [e.to_dict() for e in self._entries.values()],
        }
