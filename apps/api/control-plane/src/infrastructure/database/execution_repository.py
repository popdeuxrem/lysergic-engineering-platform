from datetime import UTC, datetime

from sqlalchemy.orm import Session

from src.domain.execution import Execution
from src.domain.execution_status import ExecutionStatus
from src.infrastructure.database.execution_model import ExecutionModel


class SqlAlchemyExecutionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, execution: Execution) -> None:
        model = self._session.get(ExecutionModel, execution.execution_id)
        if model is None:
            model = ExecutionModel(
                id=execution.execution_id,
                status=execution.status.value,
                created_at=execution.created_at,
                updated_at=execution.updated_at,
            )
            self._session.add(model)
        else:
            model.status = execution.status.value
            model.updated_at = datetime.now(UTC)
        self._session.commit()

    def get_by_id(self, execution_id: str) -> Execution | None:
        model = self._session.get(ExecutionModel, execution_id)
        if model is None:
            return None
        return Execution.reconstitute(
            execution_id=model.id,
            status=ExecutionStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
