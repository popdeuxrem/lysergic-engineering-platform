from fastapi import APIRouter, status
from sqlalchemy.orm import Session

from src.api.v1.schemas.execution import (
    CreateExecutionResponse,
    GetExecutionResponse,
    TransitionExecutionRequest,
    TransitionExecutionResponse,
)
from src.application.execution_dto import (
    CreateExecutionCommand,
    GetExecutionQuery,
    TransitionExecutionCommand,
)
from src.application.execution_use_cases import (
    CreateExecutionUseCase,
    GetExecutionUseCase,
    TransitionExecutionStateUseCase,
)
from src.infrastructure.database.execution_repository import SqlAlchemyExecutionRepository
from src.infrastructure.database.session import SessionLocal

router = APIRouter(prefix="/executions", tags=["executions"])


def _get_session() -> Session:
    return SessionLocal()


def _create_repo(session: Session) -> SqlAlchemyExecutionRepository:
    return SqlAlchemyExecutionRepository(session)


@router.post("", response_model=CreateExecutionResponse, status_code=status.HTTP_201_CREATED)
def create_execution() -> CreateExecutionResponse:
    session = _get_session()
    try:
        use_case = CreateExecutionUseCase(_create_repo(session))
        result = use_case.execute(CreateExecutionCommand())
        return CreateExecutionResponse(
            execution_id=result.execution_id,
            status=result.status,
            created_at=result.created_at,
        )
    finally:
        session.close()


@router.get("/{execution_id}", response_model=GetExecutionResponse)
def get_execution(execution_id: str) -> GetExecutionResponse:
    session = _get_session()
    try:
        use_case = GetExecutionUseCase(_create_repo(session))
        result = use_case.execute(GetExecutionQuery(execution_id=execution_id))
        return GetExecutionResponse(
            execution_id=result.execution_id,
            status=result.status,
            created_at=result.created_at,
            updated_at=result.updated_at,
        )
    finally:
        session.close()


@router.post("/{execution_id}/transition", response_model=TransitionExecutionResponse)
def transition_execution(
    execution_id: str, body: TransitionExecutionRequest
) -> TransitionExecutionResponse:
    session = _get_session()
    try:
        use_case = TransitionExecutionStateUseCase(_create_repo(session))
        result = use_case.execute(
            TransitionExecutionCommand(execution_id=execution_id, target_status=body.target_status)
        )
        return TransitionExecutionResponse(
            execution_id=result.execution_id,
            status=result.status,
            updated_at=result.updated_at,
        )
    finally:
        session.close()
