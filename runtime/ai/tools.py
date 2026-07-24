from __future__ import annotations

from typing import Any

from runtime.ai.exceptions import PermissionDeniedError


class ToolInvocation:
    def __init__(self) -> None:
        self._tools: dict[str, dict[str, Any]] = {}

    def register_tool(self, tool_id: str, handler: Any, description: str = "", source: str = "") -> None:
        self._tools[tool_id] = {"handler": handler, "description": description, "source": source}

    def invoke(self, tool_id: str, agent_id: str, allowed_tools: set[str], input_data: Any = None) -> Any:
        if tool_id not in allowed_tools:
            raise PermissionDeniedError(agent_id, f"tool:{tool_id}")
        tool = self._tools.get(tool_id)
        if tool is None:
            raise ValueError(f"Tool not found: {tool_id}")
        handler = tool["handler"]
        if callable(handler):
            return handler(input_data)
        return handler

    def list_tools(self) -> tuple[dict[str, Any], ...]:
        return tuple({"tool_id": tid, "description": t["description"], "source": t["source"]} for tid, t in self._tools.items())

    @property
    def tool_count(self) -> int:
        return len(self._tools)
