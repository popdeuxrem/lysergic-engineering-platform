from src.application.exceptions import ServiceError
from src.application.execution_dto import (
    CreateExecutionCommand,
    CreateExecutionResult,
    GetExecutionQuery,
    GetExecutionResult,
    TransitionExecutionCommand,
    TransitionExecutionResult,
)
from src.domain.execution import Execution
from src.domain.execution_status import ExecutionStatus
from src.domain.repository import ExecutionRepository


class CreateExecutionUseCase:
    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository

    def execute(self, command: CreateExecutionCommand) -> CreateExecutionResult:
        execution = Execution()
        self._repository.save(execution)
        return CreateExecutionResult(
            execution_id=execution.execution_id,
            status=execution.status,
            created_at=execution.created_at,
        )


class GetExecutionUseCase:
    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository

    def execute(self, query: GetExecutionQuery) -> GetExecutionResult:
        execution = self._repository.get_by_id(query.execution_id)
        if execution is None:
            raise ServiceError(f"Execution {query.execution_id} not found")
        return GetExecutionResult(
            execution_id=execution.execution_id,
            status=execution.status,
            created_at=execution.created_at,
            updated_at=execution.updated_at,
        )


class TransitionExecutionStateUseCase:
    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository

    def execute(self, command: TransitionExecutionCommand) -> TransitionExecutionResult:
        execution = self._repository.get_by_id(command.execution_id)
        if execution is None:
            raise ServiceError(f"Execution {command.execution_id} not found")

        if command.target_status == ExecutionStatus.RUNNING:
            execution.start()
        elif command.target_status == ExecutionStatus.COMPLETED:
            execution.complete()
        elif command.target_status == ExecutionStatus.FAILED:
            execution.fail()
        else:
            raise ServiceError(f"Unsupported target status: {command.target_status}")

        self._repository.save(execution)
        return TransitionExecutionResult(
            execution_id=execution.execution_id,
            status=execution.status,
            updated_at=execution.updated_at,
        )
