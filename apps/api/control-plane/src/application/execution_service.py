from src.application.dto.execution_projection import ExecutionProjection
from src.application.execution_dto import (
    CreateExecutionCommand,
    CreateExecutionResult,
    TransitionExecutionCommand,
    TransitionExecutionResult,
)
from src.application.execution_use_cases import (
    CreateExecutionUseCase,
    TransitionExecutionStateUseCase,
)
from src.application.queries.execution_queries import GetExecutionQuery
from src.application.queries.handlers.execution_query_handler import ExecutionQueryHandler
from src.domain.execution_status import ExecutionStatus
from src.domain.repository import ExecutionRepository


class ExecutionService:
    """Application service coordinating execution operations.

    Provides a unified boundary for API consumers to interact with
    the execution domain while preserving command/query separation.
    """

    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository
        self._query_handler = ExecutionQueryHandler(repository)

    def create(self) -> CreateExecutionResult:
        use_case = CreateExecutionUseCase(self._repository)
        return use_case.execute(CreateExecutionCommand())

    def get(self, execution_id: str) -> ExecutionProjection:
        projection = self._query_handler.handle(GetExecutionQuery(execution_id=execution_id))
        if projection is None:
            from src.application.exceptions import ServiceError
            raise ServiceError(f"Execution {execution_id} not found")
        return projection

    def transition(self, execution_id: str, target_status: ExecutionStatus) -> TransitionExecutionResult:
        use_case = TransitionExecutionStateUseCase(self._repository)
        return use_case.execute(
            TransitionExecutionCommand(execution_id=execution_id, target_status=target_status)
        )
