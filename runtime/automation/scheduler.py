from __future__ import annotations

from datetime import UTC, datetime, timedelta


class ScheduleEntry:
    def __init__(self, schedule_id: str, automation_id: str, interval_seconds: int = 0) -> None:
        self.schedule_id = schedule_id
        self.automation_id = automation_id
        self.interval_seconds = interval_seconds
        self.last_run: datetime | None = None
        self.next_run: datetime | None = datetime.now(UTC) + timedelta(seconds=interval_seconds) if interval_seconds > 0 else None

    def is_due(self) -> bool:
        if self.next_run is None:
            return False
        return datetime.now(UTC) >= self.next_run

    def mark_run(self) -> None:
        self.last_run = datetime.now(UTC)
        if self.interval_seconds > 0:
            self.next_run = datetime.now(UTC) + timedelta(seconds=self.interval_seconds)
        else:
            self.next_run = None


class Scheduler:
    def __init__(self) -> None:
        self._schedules: dict[str, ScheduleEntry] = {}

    def register(self, schedule_id: str, automation_id: str, interval_seconds: int = 0) -> ScheduleEntry:
        entry = ScheduleEntry(schedule_id, automation_id, interval_seconds)
        self._schedules[schedule_id] = entry
        return entry

    def remove(self, schedule_id: str) -> bool:
        return self._schedules.pop(schedule_id, None) is not None

    def due_automations(self) -> tuple[str, ...]:
        return tuple(entry.automation_id for entry in self._schedules.values() if entry.is_due())

    def mark_run(self, schedule_id: str) -> None:
        entry = self._schedules.get(schedule_id)
        if entry is not None:
            entry.mark_run()

    @property
    def entries(self) -> tuple[ScheduleEntry, ...]:
        return tuple(self._schedules.values())

    @property
    def count(self) -> int:
        return len(self._schedules)
