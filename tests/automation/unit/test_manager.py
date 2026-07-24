from runtime.automation.manager import AutomationManager
from runtime.automation.model import (
    AutomationAction,
)
from runtime.services.events import EventBus


def test_initial_state() -> None:
    m = AutomationManager()
    assert m.manager_status.name == "PENDING"


def test_initialize() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    assert m.manager_status.name == "READY"


def test_create() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    a = m.create("a-1", "Deploy", version="1.0.0")
    assert a.automation_id == "a-1"
    assert m.get("a-1") is not None


def test_validate() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    m.create("a-1", "Deploy")
    m.validate_automation("a-1")
    assert m.status("a-1") == "validated"


def test_ready() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    m.create("a-1", "Deploy")
    m.validate_automation("a-1")
    m.ready_automation("a-1")
    assert m.status("a-1") == "ready"


def test_enable() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    actions = (AutomationAction(action_id="a1", target="workflow"),)
    m.create("a-1", "Deploy", actions=actions)
    m.validate_automation("a-1")
    m.ready_automation("a-1")
    m.enable("a-1")
    assert m.status("a-1") == "enabled"


def test_disable() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    actions = (AutomationAction(action_id="a1", target="workflow"),)
    m.create("a-1", "Deploy", actions=actions)
    m.validate_automation("a-1")
    m.ready_automation("a-1")
    m.enable("a-1")
    m.disable("a-1")
    assert m.status("a-1") == "disabled"


def test_execute() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    actions = (AutomationAction(action_id="a1", target="workflow"),)
    m.create("a-1", "Deploy", actions=actions)
    m.validate_automation("a-1")
    m.ready_automation("a-1")
    m.enable("a-1")
    result = m.execute("a-1", "manual")
    assert result is not None and result.status == "completed"


def test_execute_missing() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    assert m.execute("missing", "manual") is None


def test_status() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    m.create("a-1", "Test")
    assert m.status("a-1") == "created"
    assert m.status("missing") is None


def test_list() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    m.create("a", "A")
    m.create("b", "B")
    assert len(m.list()) == 2


def test_history() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    actions = (AutomationAction(action_id="a1", target="workflow"),)
    m.create("a-1", "Deploy", actions=actions)
    m.validate_automation("a-1")
    m.ready_automation("a-1")
    m.enable("a-1")
    m.execute("a-1", "manual")
    assert len(m.history("a-1")) == 1


def test_archive() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    m.create("a-1", "Test")
    m.archive("a-1")
    assert m.status("a-1") == "archived"


def test_snapshot() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    m.create("a-1", "Test")
    snap = m.snapshot_state()
    assert snap.count() == 1


def test_events() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))
    m = AutomationManager(event_bus=bus)
    m.initialize_runtime()
    m.create("a-1", "Test")
    assert "automation.AutomationCreated" in events


def test_shutdown() -> None:
    m = AutomationManager()
    m.initialize_runtime()
    m.create("a-1", "Test")
    m.shutdown()
    assert m.get("a-1") is None
