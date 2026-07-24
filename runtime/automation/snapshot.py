from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.automation.model import Automation


class AutomationSnapshot:
    def __init__(self, automations: dict[str, Automation], version: int = 0) -> None:
        self._automations = dict(automations)
        self._version = version
        self._timestamp = datetime.now(UTC)

    def get(self, automation_id: str) -> Automation | None:
        return self._automations.get(automation_id)

    def list(self) -> tuple[Automation, ...]:
        return tuple(self._automations.values())

    def count(self) -> int:
        return len(self._automations)

    @property
    def version(self) -> int:
        return self._version

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> dict[str, Any]:
        return {"version": self._version, "timestamp": self._timestamp.isoformat(), "automations": [a.automation_id for a in self._automations.values()]}
