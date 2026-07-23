from fastapi import APIRouter, status
from sqlalchemy.orm import Session

from src.api.v1.schemas.execution import (
    CreateExecutionResponse,
    TransitionExecutionRequest,
    TransitionExecutionResponse,
)
from src.application.audit.handlers.execution_audit_handler import ExecutionAuditHandler
from src.application.dto.execution_projection import ExecutionProjection
from src.application.execution_service import ExecutionService
from src.infrastructure.database.execution_repository import (
    SqlAlchemyExecutionRepository,
)
from src.infrastructure.database.session import create_session

router = APIRouter(prefix="/executions", tags=["executions"])


def _get_service(session: Session) -> ExecutionService:
    return ExecutionService(SqlAlchemyExecutionRepository(session))


@router.post("", response_model=CreateExecutionResponse, status_code=status.HTTP_201_CREATED)
def create_execution() -> CreateExecutionResponse:
    session = create_session()
    try:
        result = _get_service(session).create()
        return CreateExecutionResponse(
            execution_id=result.execution_id,
            status=result.status,
            created_at=result.created_at,
        )
    finally:
        session.close()


@router.get("/{execution_id}", response_model=ExecutionProjection)
def get_execution(execution_id: str) -> ExecutionProjection:
    session = create_session()
    try:
        result = _get_service(session).get(execution_id)
        return result
    finally:
        session.close()


@router.post("/{execution_id}/transition", response_model=TransitionExecutionResponse)
def transition_execution(
    execution_id: str, body: TransitionExecutionRequest
) -> TransitionExecutionResponse:
    session = create_session()
    try:
        result = _get_service(session).transition(execution_id, body.target_status)
        return TransitionExecutionResponse(
            execution_id=result.execution_id,
            status=result.status,
            updated_at=result.updated_at,
        )
    finally:
        session.close()


@router.get("/{execution_id}/audit")
def audit_execution(execution_id: str) -> dict[str, object]:
    session = create_session()
    try:
        repo = SqlAlchemyExecutionRepository(session)
        handler = ExecutionAuditHandler(repo)
        result = handler.audit_by_id(execution_id)
        if result is None:
            return {"execution_id": execution_id, "valid": False, "issues": ["not found"]}
        return result.model_dump()
    finally:
        session.close()
