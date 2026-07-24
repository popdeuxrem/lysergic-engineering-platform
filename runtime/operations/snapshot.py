from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.operations.model import EngineeringOperation


class OperationsSnapshot:
    def __init__(self, operations: dict[str, EngineeringOperation], version: int = 0) -> None:
        self._operations = dict(operations)
        self._version = version
        self._timestamp = datetime.now(UTC)

    def get(self, op_id: str) -> EngineeringOperation | None:
        return self._operations.get(op_id)

    def list(self) -> tuple[EngineeringOperation, ...]:
        return tuple(self._operations.values())

    def count(self) -> int:
        return len(self._operations)

    @property
    def version(self) -> int:
        return self._version

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> dict[str, Any]:
        return {"version": self._version, "timestamp": self._timestamp.isoformat(), "operations": [o.operation_id for o in self._operations.values()]}
