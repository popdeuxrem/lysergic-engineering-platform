from __future__ import annotations

from runtime.operations.exceptions import OperationConflictError, RegistryFrozenError
from runtime.operations.model import EngineeringOperation


class OperationsRegistry:
    def __init__(self) -> None:
        self._operations: dict[str, EngineeringOperation] = {}
        self._frozen = False

    def register(self, op: EngineeringOperation) -> None:
        if self._frozen:
            raise RegistryFrozenError()
        if op.operation_id in self._operations:
            raise OperationConflictError(op.operation_id)
        self._operations[op.operation_id] = op

    def get(self, op_id: str) -> EngineeringOperation | None:
        return self._operations.get(op_id)

    def unregister(self, op_id: str) -> bool:
        if self._frozen:
            raise RegistryFrozenError()
        return self._operations.pop(op_id, None) is not None

    def list(self) -> tuple[EngineeringOperation, ...]:
        return tuple(self._operations.values())

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def count(self) -> int:
        return len(self._operations)

    def __contains__(self, op_id: str) -> bool:
        return op_id in self._operations
