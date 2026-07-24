from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.ai.model import Agent


class AISnapshot:
    def __init__(self, agents: dict[str, Agent], version: int = 0) -> None:
        self._agents = dict(agents)
        self._version = version
        self._timestamp = datetime.now(UTC)

    def get(self, agent_id: str) -> Agent | None:
        return self._agents.get(agent_id)

    def list(self) -> tuple[Agent, ...]:
        return tuple(self._agents.values())

    def count(self) -> int:
        return len(self._agents)

    @property
    def version(self) -> int:
        return self._version

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> dict[str, Any]:
        return {"version": self._version, "timestamp": self._timestamp.isoformat(), "agents": [a.agent_id for a in self._agents.values()]}
