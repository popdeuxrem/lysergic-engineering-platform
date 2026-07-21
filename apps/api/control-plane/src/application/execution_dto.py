from dataclasses import dataclass
from datetime import datetime

from src.application.dto import Command, Query, Result
from src.domain.execution_status import ExecutionStatus


@dataclass(frozen=True)
class CreateExecutionCommand(Command):
    pass


@dataclass(frozen=True)
class CreateExecutionResult(Result):
    execution_id: str
    status: ExecutionStatus
    created_at: datetime


@dataclass(frozen=True)
class GetExecutionQuery(Query):
    execution_id: str


@dataclass(frozen=True)
class GetExecutionResult(Result):
    execution_id: str
    status: ExecutionStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class TransitionExecutionCommand(Command):
    execution_id: str
    target_status: ExecutionStatus


@dataclass(frozen=True)
class TransitionExecutionResult(Result):
    execution_id: str
    status: ExecutionStatus
    updated_at: datetime
