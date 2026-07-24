from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class MemoryEntry:
    key: str
    value: Any = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class AgentMemory:
    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._history: dict[str, list[MemoryEntry]] = {}

    def create_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = {}
            self._history[session_id] = []

    def set(self, session_id: str, key: str, value: Any) -> None:
        self._ensure_session(session_id)
        self._sessions[session_id][key] = value
        self._history[session_id].append(MemoryEntry(key=key, value=value))

    def get(self, session_id: str, key: str) -> Any | None:
        session = self._sessions.get(session_id)
        return session.get(key) if session else None

    def clear_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        self._history.pop(session_id, None)

    def session_history(self, session_id: str) -> tuple[MemoryEntry, ...]:
        return tuple(self._history.get(session_id, []))

    @property
    def active_sessions(self) -> tuple[str, ...]:
        return tuple(self._sessions.keys())

    def _ensure_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            self.create_session(session_id)
