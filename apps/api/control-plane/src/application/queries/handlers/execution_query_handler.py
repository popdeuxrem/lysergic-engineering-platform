from src.application.dto.execution_projection import ExecutionProjection
from src.application.queries.execution_queries import GetExecutionQuery
from src.domain.repository import ExecutionRepository


class ExecutionQueryHandler:
    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository

    def handle(self, query: GetExecutionQuery) -> ExecutionProjection | None:
        execution = self._repository.get_by_id(query.execution_id)
        if execution is None:
            return None
        return ExecutionProjection(
            execution_id=execution.execution_id,
            status=execution.status,
            created_at=execution.created_at,
            updated_at=execution.updated_at,
        )
