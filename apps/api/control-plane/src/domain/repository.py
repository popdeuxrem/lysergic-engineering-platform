from typing import Protocol

from src.domain.execution import Execution


class ExecutionRepository(Protocol):
    def save(self, execution: Execution) -> None: ...
    def get_by_id(self, execution_id: str) -> Execution | None: ...
