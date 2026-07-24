from runtime.automation.model import Automation
from runtime.automation.registry import AutomationRegistry


def test_register() -> None:
    r = AutomationRegistry()
    r.register(Automation(automation_id="a-1", name="Test", version="1.0.0"))
    assert "a-1" in r
    assert r.count == 1


def test_duplicate_raises() -> None:
    r = AutomationRegistry()
    r.register(Automation(automation_id="a-1", name="T", version="1.0.0"))
    try:
        r.register(Automation(automation_id="a-1", name="T", version="1.0.0"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_get() -> None:
    r = AutomationRegistry()
    a = Automation(automation_id="a-1", name="T", version="1.0.0")
    r.register(a)
    assert r.get("a-1") is a
    assert r.get("missing") is None


def test_unregister() -> None:
    r = AutomationRegistry()
    r.register(Automation(automation_id="a", name="A", version="1.0.0"))
    assert r.unregister("a") is True
    assert r.count == 0


def test_list() -> None:
    r = AutomationRegistry()
    r.register(Automation(automation_id="a", name="A", version="1.0.0"))
    r.register(Automation(automation_id="b", name="B", version="2.0.0"))
    assert len(r.list()) == 2


def test_list_by_trigger() -> None:
    from runtime.automation.model import TriggerDefinition
    triggers = (TriggerDefinition(trigger_id="t1", trigger_type="event"),)
    r = AutomationRegistry()
    r.register(Automation(automation_id="a", name="A", version="1.0.0", triggers=triggers))
    r.register(Automation(automation_id="b", name="B", version="1.0.0"))
    assert len(r.list_by_trigger("event")) == 1


def test_freeze() -> None:
    r = AutomationRegistry()
    r.freeze()
    try:
        r.register(Automation(automation_id="late", name="Late", version="1.0.0"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass
