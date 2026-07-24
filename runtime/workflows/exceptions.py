class WorkflowError(Exception):
    pass

class WorkflowNotFoundError(WorkflowError):
    def __init__(self, workflow_id: str) -> None:
        self.workflow_id = workflow_id
        super().__init__(f"Workflow not found: {workflow_id}")

class WorkflowConflictError(WorkflowError):
    def __init__(self, workflow_id: str) -> None:
        self.workflow_id = workflow_id
        super().__init__(f"Workflow already exists: {workflow_id}")

class InvalidTransitionError(WorkflowError):
    def __init__(self, current: str, target: str) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Invalid transition: {current} -> {target}")

class ExecutionError(WorkflowError):
    def __init__(self, workflow_id: str, step: str, message: str) -> None:
        self.workflow_id = workflow_id
        self.step = step
        super().__init__(f"Execution failed for {workflow_id} step {step}: {message}")

class ValidationError(WorkflowError):
    def __init__(self, workflow_id: str, errors: tuple[str, ...]) -> None:
        self.workflow_id = workflow_id
        self.errors = errors
        super().__init__(f"Validation failed for {workflow_id}: {'; '.join(errors)}")

class RegistryFrozenError(WorkflowError):
    def __init__(self) -> None:
        super().__init__("Workflow registry is frozen")
