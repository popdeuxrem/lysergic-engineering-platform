from runtime.ai.planner import Planner, PlanStep


def test_create_plan() -> None:
    p = Planner()
    steps = (PlanStep(step_id="s1", objective="validate"), PlanStep(step_id="s2", objective="deploy"))
    plan = p.create_plan("plan-1", "deploy system", steps)
    assert plan.plan_id == "plan-1"
    assert len(plan.steps) == 2


def test_get_plan() -> None:
    p = Planner()
    p.create_plan("plan-1", "objective")
    plan = p.get_plan("plan-1")
    assert plan is not None and plan.objective == "objective"


def test_decompose() -> None:
    p = Planner()
    parts = p.decompose("step1.step2.step3")
    assert len(parts) == 3
