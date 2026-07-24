from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class StepType(Enum):
    TASK = "task"
    CONDITIONAL = "conditional"
    PARALLEL = "parallel"
    SUB_WORKFLOW = "sub_workflow"


@dataclass(frozen=True)
class WorkflowStep:
    step_id: str
    name: str
    step_type: StepType = StepType.TASK
    description: str = ""
    contract: str = ""
    timeout_seconds: int = 0
    retry_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowDefinition:
    workflow_id: str
    name: str
    version: str = "0.1.0"
    description: str = ""
    steps: tuple[WorkflowStep, ...] = ()
    owner: str = ""
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    def step_count(self) -> int:
        return len(self.steps)

    def step_ids(self) -> tuple[str, ...]:
        return tuple(s.step_id for s in self.steps)


@dataclass
class StepResult:
    step_id: str
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    output: Any = None
    error: str = ""


@dataclass
class WorkflowExecution:
    execution_id: str
    workflow_id: str
    status: str = "pending"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    step_results: tuple[StepResult, ...] = ()
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowResult:
    execution_id: str
    workflow_id: str
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    step_results: tuple[StepResult, ...] = ()
    error: str = ""

    def successful(self) -> bool:
        return self.status == "completed"

    def failed(self) -> bool:
        return self.status == "failed"

    def duration_seconds(self) -> float:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0
