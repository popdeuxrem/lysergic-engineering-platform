from __future__ import annotations

from runtime.ai.exceptions import PermissionDeniedError


class AgentPermissions:
    def __init__(self) -> None:
        self._allowed_tools: dict[str, set[str]] = {}
        self._allowed_knowledge: dict[str, set[str]] = {}
        self._allowed_projects: dict[str, set[str]] = {}
        self._deny_by_default = True

    def configure(self, agent_id: str, tools: set[str] | None = None, knowledge: set[str] | None = None, projects: set[str] | None = None) -> None:
        if tools is not None:
            self._allowed_tools[agent_id] = tools
        if knowledge is not None:
            self._allowed_knowledge[agent_id] = knowledge
        if projects is not None:
            self._allowed_projects[agent_id] = projects

    def can_access_tool(self, agent_id: str, tool_id: str) -> bool:
        allowed = self._allowed_tools.get(agent_id, set())
        return tool_id in allowed

    def can_access_knowledge(self, agent_id: str, knowledge_id: str) -> bool:
        allowed = self._allowed_knowledge.get(agent_id, set())
        return knowledge_id in allowed

    def can_access_project(self, agent_id: str, project_id: str) -> bool:
        allowed = self._allowed_projects.get(agent_id, set())
        return project_id in allowed

    def enforce_tool(self, agent_id: str, tool_id: str) -> None:
        if not self.can_access_tool(agent_id, tool_id):
            raise PermissionDeniedError(agent_id, f"tool:{tool_id}")

    def revoke(self, agent_id: str) -> None:
        self._allowed_tools.pop(agent_id, None)
        self._allowed_knowledge.pop(agent_id, None)
        self._allowed_projects.pop(agent_id, None)
