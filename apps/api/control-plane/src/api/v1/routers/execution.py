from fastapi import APIRouter, status
from sqlalchemy.orm import Session

from src.api.v1.schemas.execution import (
    CreateExecutionResponse,
    GetExecutionResponse,
    TransitionExecutionRequest,
    TransitionExecutionResponse,
)
from src.application.execution_service import ExecutionService
from src.infrastructure.database.execution_repository import SqlAlchemyExecutionRepository
from src.infrastructure.database.session import SessionLocal

router = APIRouter(prefix="/executions", tags=["executions"])


def _get_service(session: Session) -> ExecutionService:
    return ExecutionService(SqlAlchemyExecutionRepository(session))


@router.post("", response_model=CreateExecutionResponse, status_code=status.HTTP_201_CREATED)
def create_execution() -> CreateExecutionResponse:
    session = SessionLocal()
    try:
        result = _get_service(session).create()
        return CreateExecutionResponse(
            execution_id=result.execution_id,
            status=result.status,
            created_at=result.created_at,
        )
    finally:
        session.close()


@router.get("/{execution_id}", response_model=GetExecutionResponse)
def get_execution(execution_id: str) -> GetExecutionResponse:
    session = SessionLocal()
    try:
        result = _get_service(session).get(execution_id)
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
    session = SessionLocal()
    try:
        result = _get_service(session).transition(execution_id, body.target_status)
        return TransitionExecutionResponse(
            execution_id=result.execution_id,
            status=result.status,
            updated_at=result.updated_at,
        )
    finally:
        session.close()
