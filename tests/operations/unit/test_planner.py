from runtime.operations.planner import OperationPlanner, PlanStep


def test_create_plan() -> None:
    p = OperationPlanner()
    steps = (PlanStep(step_id="s1", objective="validate"), PlanStep(step_id="s2", objective="deploy"))
    plan = p.create_plan("plan-1", "deploy system", steps)
    assert plan.plan_id == "plan-1"
    assert len(plan.steps) == 2


def test_get_plan() -> None:
    p = OperationPlanner()
    p.create_plan("plan-1", "obj")
    assert p.get_plan("plan-1") is not None


def test_decompose() -> None:
    p = OperationPlanner()
    parts = p.decompose("validate, deploy, verify")
    assert len(parts) == 3
