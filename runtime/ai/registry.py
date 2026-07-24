from __future__ import annotations

from runtime.ai.exceptions import AgentConflictError, RegistryFrozenError
from runtime.ai.model import Agent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}
        self._frozen = False

    def register(self, agent: Agent) -> None:
        if self._frozen:
            raise RegistryFrozenError()
        if agent.agent_id in self._agents:
            raise AgentConflictError(agent.agent_id)
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Agent | None:
        return self._agents.get(agent_id)

    def unregister(self, agent_id: str) -> bool:
        if self._frozen:
            raise RegistryFrozenError()
        return self._agents.pop(agent_id, None) is not None

    def list(self) -> tuple[Agent, ...]:
        return tuple(self._agents.values())

    def list_by_capability(self, capability_id: str) -> tuple[Agent, ...]:
        return tuple(a for a in self._agents.values() if any(c.capability_id == capability_id for c in a.capabilities))

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def count(self) -> int:
        return len(self._agents)

    def __contains__(self, agent_id: str) -> bool:
        return agent_id in self._agents
