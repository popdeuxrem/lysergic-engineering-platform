from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any


class AgentLifecycleState(Enum):
    CREATED = "created"
    REGISTERED = "registered"
    VALIDATED = "validated"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ARCHIVED = "archived"
    FAILED = "failed"


_AGENT_TRANSITIONS: dict[AgentLifecycleState, tuple[AgentLifecycleState, ...]] = {
    AgentLifecycleState.CREATED: (AgentLifecycleState.REGISTERED, AgentLifecycleState.FAILED, AgentLifecycleState.ARCHIVED),
    AgentLifecycleState.REGISTERED: (AgentLifecycleState.VALIDATED, AgentLifecycleState.FAILED, AgentLifecycleState.ARCHIVED),
    AgentLifecycleState.VALIDATED: (AgentLifecycleState.READY, AgentLifecycleState.FAILED, AgentLifecycleState.ARCHIVED),
    AgentLifecycleState.READY: (AgentLifecycleState.RUNNING, AgentLifecycleState.STOPPED, AgentLifecycleState.FAILED, AgentLifecycleState.ARCHIVED),
    AgentLifecycleState.RUNNING: (AgentLifecycleState.PAUSED, AgentLifecycleState.STOPPED, AgentLifecycleState.FAILED),
    AgentLifecycleState.PAUSED: (AgentLifecycleState.RUNNING, AgentLifecycleState.STOPPED, AgentLifecycleState.FAILED),
    AgentLifecycleState.STOPPED: (AgentLifecycleState.READY, AgentLifecycleState.ARCHIVED, AgentLifecycleState.FAILED),
    AgentLifecycleState.ARCHIVED: (AgentLifecycleState.CREATED,),
    AgentLifecycleState.FAILED: (AgentLifecycleState.CREATED, AgentLifecycleState.ARCHIVED),
}


class AgentLifecycle:
    def __init__(self) -> None:
        self._states: dict[str, AgentLifecycleState] = {}
        self._transitions: list[dict[str, Any]] = []

    def initialize(self, agent_id: str) -> None:
        self._states[agent_id] = AgentLifecycleState.CREATED
        self._record(agent_id, AgentLifecycleState.CREATED)

    def transition(self, agent_id: str, target: AgentLifecycleState) -> None:
        current = self._states.get(agent_id)
        if current is None:
            raise KeyError(f"Agent not found: {agent_id}")
        allowed = _AGENT_TRANSITIONS.get(current, ())
        if target not in allowed:
            from runtime.ai.exceptions import InvalidLifecycleError
            raise InvalidLifecycleError(current.value, target.value)
        self._states[agent_id] = target
        self._record(agent_id, target)

    def state_of(self, agent_id: str) -> AgentLifecycleState | None:
        return self._states.get(agent_id)

    def can_transition(self, agent_id: str, target: AgentLifecycleState) -> bool:
        current = self._states.get(agent_id)
        return current is not None and target in _AGENT_TRANSITIONS.get(current, ())

    @property
    def history(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._transitions)

    def _record(self, agent_id: str, state: AgentLifecycleState) -> None:
        self._transitions.append({"agent_id": agent_id, "state": state.value, "timestamp": datetime.now(UTC).isoformat()})
