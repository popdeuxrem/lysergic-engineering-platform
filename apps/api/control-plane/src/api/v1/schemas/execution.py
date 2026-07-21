from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.execution_status import ExecutionStatus


class CreateExecutionResponse(BaseModel):
    execution_id: str = Field(examples=["550e8400-e29b-41d4-a716-446655440000"])
    status: ExecutionStatus
    created_at: datetime


class GetExecutionResponse(BaseModel):
    execution_id: str
    status: ExecutionStatus
    created_at: datetime
    updated_at: datetime


class TransitionExecutionRequest(BaseModel):
    target_status: ExecutionStatus


class TransitionExecutionResponse(BaseModel):
    execution_id: str
    status: ExecutionStatus
    updated_at: datetime
