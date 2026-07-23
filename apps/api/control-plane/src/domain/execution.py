from datetime import UTC, datetime, timezone
from uuid import uuid4

from src.domain.entities import Entity
from src.domain.execution_status import ExecutionStatus


class Execution(Entity):
    def __init__(self, execution_id: str | None = None) -> None:
        self._id = execution_id or str(uuid4())
        self._status: ExecutionStatus = ExecutionStatus.CREATED
        self._created_at: datetime = datetime.now(UTC)
        self._updated_at: datetime = self._created_at

    @property
    def execution_id(self) -> str:
        return str(self._id)

    @property
    def status(self) -> ExecutionStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def start(self) -> None:
        self._transition_to(ExecutionStatus.RUNNING)

    def complete(self) -> None:
        self._transition_to(ExecutionStatus.COMPLETED)

    def fail(self) -> None:
        self._transition_to(ExecutionStatus.FAILED)

    @classmethod
    def reconstitute(
        cls,
        execution_id: str,
        status: ExecutionStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> "Execution":
        execution = cls.__new__(cls)
        execution._id = execution_id
        execution._status = status
        execution._created_at = created_at
        execution._updated_at = updated_at
        return execution

    def _transition_to(self, target: ExecutionStatus) -> None:
        if not self._status.can_transition_to(target):
            raise InvalidExecutionTransition(
                execution_id=self.execution_id,
                current=self._status,
                target=target,
            )
        self._status = target
        self._updated_at = datetime.now(UTC)


class InvalidExecutionTransition(Exception):
    def __init__(self, execution_id: str, current: ExecutionStatus, target: ExecutionStatus) -> None:
        self.execution_id = execution_id
        self.current = current
        self.target = target
        super().__init__(
            f"Invalid transition for execution {execution_id}: {current.value} -> {target.value}"
        )
