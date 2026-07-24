from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class ConfigSnapshot:
    config: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    source: str = "unknown"
    version: int = 0
    profile: str | None = None

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        current: Any = self.config
        for k in keys:
            if not isinstance(current, dict):
                return default
            val = current.get(k)
            if val is None:
                return default
            current = val
        return current

    def has(self, key: str) -> bool:
        return self.get(key, _MISSING) is not _MISSING

    def to_dict(self) -> dict[str, Any]:
        return {
            "config": self.config,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "version": self.version,
            "profile": self.profile,
        }

    @property
    def frozen(self) -> bool:
        return True


_MISSING = object()
