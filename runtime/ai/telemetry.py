from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class TelemetryRecord:
    agent_id: str
    event_type: str
    duration_ms: float = 0.0
    success: bool = True
    error: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class Telemetry:
    def __init__(self) -> None:
        self._records: list[TelemetryRecord] = []

    def record(self, agent_id: str, event_type: str, duration_ms: float = 0.0, success: bool = True, error: str = "") -> None:
        self._records.append(TelemetryRecord(agent_id=agent_id, event_type=event_type, duration_ms=duration_ms, success=success, error=error))

    def agent_history(self, agent_id: str) -> tuple[TelemetryRecord, ...]:
        return tuple(r for r in self._records if r.agent_id == agent_id)

    def failures(self, agent_id: str) -> tuple[TelemetryRecord, ...]:
        return tuple(r for r in self._records if r.agent_id == agent_id and not r.success)

    @property
    def total_executions(self) -> int:
        return len(self._records)

    @property
    def total_failures(self) -> int:
        return sum(1 for r in self._records if not r.success)
