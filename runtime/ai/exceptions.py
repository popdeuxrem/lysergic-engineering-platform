class AIError(Exception):
    pass

class AgentNotFoundError(AIError):
    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        super().__init__(f"Agent not found: {agent_id}")

class AgentConflictError(AIError):
    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        super().__init__(f"Agent already exists: {agent_id}")

class InvalidLifecycleError(AIError):
    def __init__(self, current: str, target: str) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Invalid lifecycle transition: {current} -> {target}")

class ExecutionError(AIError):
    def __init__(self, agent_id: str, message: str) -> None:
        super().__init__(f"Execution failed for agent '{agent_id}': {message}")

class PermissionDeniedError(AIError):
    def __init__(self, agent_id: str, resource: str) -> None:
        super().__init__(f"Agent '{agent_id}' denied access to: {resource}")

class RegistryFrozenError(AIError):
    def __init__(self) -> None:
        super().__init__("Agent registry is frozen")
