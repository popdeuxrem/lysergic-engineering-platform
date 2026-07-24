from runtime.automation.executor import AutomationExecutor
from runtime.automation.model import Automation, AutomationAction


def test_execute() -> None:
    ex = AutomationExecutor()
    actions = (AutomationAction(action_id="a1", target="workflow"),)
    a = Automation(automation_id="a-1", name="Test", version="1.0.0", actions=actions)
    result = ex.execute(a, "manual")
    assert result.status == "completed"
    assert "1 action(s)" in result.result


def test_execute_no_actions() -> None:
    ex = AutomationExecutor()
    a = Automation(automation_id="a-1", name="Test", version="1.0.0")
    result = ex.execute(a)
    assert result.status == "failed"


def test_history() -> None:
    ex = AutomationExecutor()
    a = Automation(automation_id="a-1", name="Test", version="1.0.0", actions=(AutomationAction(action_id="a1", target="workflow"),))
    ex.execute(a)
    assert ex.execution_count == 1
