from runtime.automation.model import (
    Automation,
    AutomationAction,
    AutomationExecution,
    ExecutionPolicy,
    TriggerDefinition,
)


def test_automation_creation() -> None:
    a = Automation(automation_id="a-1", name="Deploy", version="1.0.0")
    assert a.automation_id == "a-1"
    assert a.name == "Deploy"


def test_automation_with_triggers() -> None:
    triggers = (TriggerDefinition(trigger_id="t1", trigger_type="event"), TriggerDefinition(trigger_id="t2", trigger_type="schedule"))
    a = Automation(automation_id="a-1", name="Test", version="1.0.0", triggers=triggers)
    assert len(a.triggers) == 2


def test_automation_with_actions() -> None:
    actions = (AutomationAction(action_id="a1", target="workflow"), AutomationAction(action_id="a2", target="ai"))
    a = Automation(automation_id="a-1", name="Test", version="1.0.0", actions=actions)
    assert len(a.actions) == 2


def test_execution_policy() -> None:
    p = ExecutionPolicy(policy_id="strict", allowed_targets=("workflow",), require_approval=True)
    assert p.require_approval is True
    assert "workflow" in p.allowed_targets


def test_execution() -> None:
    e = AutomationExecution(execution_id="e1", automation_id="a-1", status="completed")
    assert e.status == "completed"
