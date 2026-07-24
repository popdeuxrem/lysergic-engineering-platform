from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

ChangeHandler = Callable[[str, Any, Any], None]


@dataclass
class WatchRegistration:
    key: str
    handler: ChangeHandler
    enabled: bool = True
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class ConfigWatcher:
    def __init__(self) -> None:
        self._watchers: dict[str, list[WatchRegistration]] = {}
        self._enabled = True

    def watch(self, key: str, handler: ChangeHandler) -> WatchRegistration:
        reg = WatchRegistration(key=key, handler=handler)
        if key not in self._watchers:
            self._watchers[key] = []
        self._watchers[key].append(reg)
        return reg

    def unwatch(self, key: str, handler: ChangeHandler) -> bool:
        if key not in self._watchers:
            return False
        before = len(self._watchers[key])
        self._watchers[key] = [w for w in self._watchers[key] if w.handler is not handler]
        return len(self._watchers[key]) < before

    def notify(self, key: str, old_value: Any, new_value: Any) -> None:
        if not self._enabled:
            return
        for registration in self._watchers.get(key, []):
            if registration.enabled:
                try:
                    registration.handler(key, old_value, new_value)
                except Exception:  # noqa: BLE001, S110
                    pass
        for registration in self._watchers.get("*", []):
            if registration.enabled:
                try:
                    registration.handler(key, old_value, new_value)
                except Exception:  # noqa: BLE001, S110
                    pass

    def disable(self) -> None:
        self._enabled = False

    def enable(self) -> None:
        self._enabled = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def count(self) -> int:
        return sum(len(ws) for ws in self._watchers.values())
