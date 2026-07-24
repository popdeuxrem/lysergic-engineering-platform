from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


class CacheEntry:
    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value
        self.cached_at = datetime.now(UTC)
        self.access_count = 0

    def access(self) -> Any:
        self.access_count += 1
        return self.value


class AssetCache:
    def __init__(self) -> None:
        self._entries: dict[str, CacheEntry] = {}
        self._enabled = True

    def get(self, key: str) -> Any | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        return entry.access()

    def set(self, key: str, value: Any) -> None:
        self._entries[key] = CacheEntry(key, value)

    def invalidate(self, key: str) -> bool:
        return self._entries.pop(key, None) is not None

    def clear(self) -> None:
        self._entries.clear()

    @property
    def enabled(self) -> bool:
        return self._enabled

    def disable(self) -> None:
        self._enabled = False

    def enable(self) -> None:
        self._enabled = True

    @property
    def size(self) -> int:
        return len(self._entries)

    @property
    def keys(self) -> tuple[str, ...]:
        return tuple(self._entries.keys())
