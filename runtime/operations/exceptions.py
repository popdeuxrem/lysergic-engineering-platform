class OperationsError(Exception):
    pass

class OperationNotFoundError(OperationsError):
    def __init__(self, op_id: str) -> None:
        self.op_id = op_id
        super().__init__(f"Operation not found: {op_id}")

class OperationConflictError(OperationsError):
    def __init__(self, op_id: str) -> None:
        self.op_id = op_id
        super().__init__(f"Operation already exists: {op_id}")

class InvalidLifecycleError(OperationsError):
    def __init__(self, current: str, target: str) -> None:
        super().__init__(f"Invalid lifecycle transition: {current} -> {target}")

class GateRejectionError(OperationsError):
    def __init__(self, op_id: str, gate: str, reason: str) -> None:
        super().__init__(f"Gate '{gate}' rejected operation '{op_id}': {reason}")

class RegistryFrozenError(OperationsError):
    def __init__(self) -> None:
        super().__init__("Operations registry is frozen")
