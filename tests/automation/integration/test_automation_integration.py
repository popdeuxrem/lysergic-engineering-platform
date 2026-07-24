from runtime.automation.manager import AutomationManager
from runtime.automation.model import AutomationAction, TriggerDefinition
from runtime.services.events import EventBus


def test_full_lifecycle() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))

    m = AutomationManager(event_bus=bus)
    m.initialize_runtime()

    triggers = (TriggerDefinition(trigger_id="t1", trigger_type="manual"),)
    actions = (AutomationAction(action_id="a1", target="workflow"),)
    m.create("a-1", "Nightly Deploy", version="1.0.0", triggers=triggers, actions=actions)
    assert "automation.AutomationCreated" in events

    m.validate_automation("a-1")
    assert "automation.AutomationValidated" in events

    m.ready_automation("a-1")
    m.enable("a-1")
    assert "automation.AutomationEnabled" in events
    assert m.status("a-1") == "enabled"

    result = m.execute("a-1", "manual")
    assert result is not None and result.status == "completed"
    assert "automation.AutomationTriggered" in events
    assert "automation.AutomationStarted" in events
    assert "automation.AutomationCompleted" in events

    m.disable("a-1")
    assert "automation.AutomationDisabled" in events
    assert m.status("a-1") == "disabled"

    assert len(m.list()) == 1
    assert len(m.history("a-1")) == 1


def test_policy_enforcement() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    actions = (AutomationAction(action_id="a1", target="unknown"),)
    m.create("a-1", "Bad", actions=actions)
    m.validate_automation("a-1")
    m.ready_automation("a-1")
    try:
        m.enable("a-1")
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_snapshot_consistency() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    m.create("a-1", "Test", version="1.0.0")
    snap = m.snapshot_state()
    assert snap.get("a-1") is not None
    assert snap.version > 0
