class AutomationError(Exception):
    pass

class AutomationNotFoundError(AutomationError):
    def __init__(self, automation_id: str) -> None:
        self.automation_id = automation_id
        super().__init__(f"Automation not found: {automation_id}")

class AutomationConflictError(AutomationError):
    def __init__(self, automation_id: str) -> None:
        self.automation_id = automation_id
        super().__init__(f"Automation already exists: {automation_id}")

class InvalidLifecycleError(AutomationError):
    def __init__(self, current: str, target: str) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Invalid lifecycle transition: {current} -> {target}")

class ExecutionError(AutomationError):
    def __init__(self, automation_id: str, message: str) -> None:
        super().__init__(f"Execution failed for automation '{automation_id}': {message}")

class PolicyDeniedError(AutomationError):
    def __init__(self, automation_id: str, policy: str) -> None:
        super().__init__(f"Policy denied automation '{automation_id}': {policy}")

class RegistryFrozenError(AutomationError):
    def __init__(self) -> None:
        super().__init__("Automation registry is frozen")
