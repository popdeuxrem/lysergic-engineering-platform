from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.execution_status import ExecutionStatus


class ExecutionProjection(BaseModel):
    model_config = {"frozen": True}

    execution_id: str = Field(examples=["550e8400-e29b-41d4-a716-446655440000"])
    status: ExecutionStatus
    created_at: datetime
    updated_at: datetime
