from src.application.execution_dto import (
    CreateExecutionCommand,
    CreateExecutionResult,
    GetExecutionQuery,
    GetExecutionResult,
    TransitionExecutionCommand,
    TransitionExecutionResult,
)
from src.application.execution_use_cases import (
    CreateExecutionUseCase,
    GetExecutionUseCase,
    TransitionExecutionStateUseCase,
)
from src.domain.execution_status import ExecutionStatus
from src.domain.repository import ExecutionRepository


class ExecutionService:
    """Application service coordinating execution operations.

    Provides a unified boundary for API consumers to interact with
    the execution domain while preserving command/query separation.
    """

    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository

    def create(self) -> CreateExecutionResult:
        use_case = CreateExecutionUseCase(self._repository)
        return use_case.execute(CreateExecutionCommand())

    def get(self, execution_id: str) -> GetExecutionResult:
        use_case = GetExecutionUseCase(self._repository)
        return use_case.execute(GetExecutionQuery(execution_id=execution_id))

    def transition(self, execution_id: str, target_status: ExecutionStatus) -> TransitionExecutionResult:
        use_case = TransitionExecutionStateUseCase(self._repository)
        return use_case.execute(
            TransitionExecutionCommand(execution_id=execution_id, target_status=target_status)
        )
