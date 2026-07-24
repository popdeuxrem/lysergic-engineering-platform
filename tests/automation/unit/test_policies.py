from runtime.automation.model import Automation, AutomationAction, ExecutionPolicy
from runtime.automation.policies import PolicyEngine


def test_check_execution_pass() -> None:
    p = PolicyEngine()
    actions = (AutomationAction(action_id="a1", target="workflow"),)
    policy = ExecutionPolicy(allowed_targets=("workflow",))
    a = Automation(automation_id="a-1", name="Test", version="1.0.0", actions=actions, policy=policy)
    p.check_execution(a)


def test_check_execution_denied() -> None:
    p = PolicyEngine()
    actions = (AutomationAction(action_id="a1", target="unknown"),)
    policy = ExecutionPolicy(allowed_targets=("workflow",))
    a = Automation(automation_id="a-1", name="Test", version="1.0.0", actions=actions, policy=policy)
    try:
        p.check_execution(a)
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_is_action_allowed() -> None:
    p = PolicyEngine()
    assert p.is_action_allowed("workflow") is True
    assert p.is_action_allowed("unknown") is False
