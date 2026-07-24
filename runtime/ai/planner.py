from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class PlanStep:
    step_id: str
    objective: str
    tool: str = ""
    input: str = ""
    depends_on: tuple[str, ...] = ()


@dataclass
class AgentPlan:
    plan_id: str
    objective: str
    steps: tuple[PlanStep, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


class Planner:
    def __init__(self) -> None:
        self._plans: dict[str, AgentPlan] = {}

    def create_plan(self, plan_id: str, objective: str, steps: tuple[PlanStep, ...] = ()) -> AgentPlan:
        plan = AgentPlan(plan_id=plan_id, objective=objective, steps=steps)
        self._plans[plan_id] = plan
        return plan

    def get_plan(self, plan_id: str) -> AgentPlan | None:
        return self._plans.get(plan_id)

    def decompose(self, objective: str) -> list[str]:
        return [s.strip() for s in objective.split(".") if s.strip()]
