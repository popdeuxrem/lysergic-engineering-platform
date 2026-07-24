from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class PlanStep:
    step_id: str
    objective: str
    target: str = ""
    target_id: str = ""


@dataclass
class ExecutionPlan:
    plan_id: str
    objective: str
    steps: tuple[PlanStep, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class OperationPlanner:
    def __init__(self) -> None:
        self._plans: dict[str, ExecutionPlan] = {}

    def create_plan(self, plan_id: str, objective: str, steps: tuple[PlanStep, ...] = ()) -> ExecutionPlan:
        plan = ExecutionPlan(plan_id=plan_id, objective=objective, steps=steps)
        self._plans[plan_id] = plan
        return plan

    def get_plan(self, plan_id: str) -> ExecutionPlan | None:
        return self._plans.get(plan_id)

    def decompose(self, objective: str) -> list[str]:
        return [s.strip() for s in objective.split(",") if s.strip()]
