from runtime.automation.model import TriggerDefinition
from runtime.automation.triggers import (
    EventTrigger,
    ManualTrigger,
    ScheduleTrigger,
    TriggerRegistry,
)


def test_event_trigger() -> None:
    t = EventTrigger("deploy")
    d = t.create_definition("t1", "code.push")
    assert d.trigger_type == "event"
    assert d.source == "code.push"


def test_schedule_trigger() -> None:
    t = ScheduleTrigger("0 */6 * * *")
    d = t.create_definition("t1", "0 */12 * * *")
    assert d.trigger_type == "schedule"
    assert d.config.get("cron") == "0 */12 * * *"


def test_manual_trigger() -> None:
    t = ManualTrigger()
    d = t.create_definition("t1")
    assert d.trigger_type == "manual"


def test_trigger_registry() -> None:
    r = TriggerRegistry()
    d = TriggerDefinition(trigger_id="t1", trigger_type="event")
    assert r.evaluate(d) is True


def test_request_execution() -> None:
    r = TriggerRegistry()
    d = TriggerDefinition(trigger_id="t1", trigger_type="event")
    r.request_execution(d)
    assert r.request_count == 1


def test_pending_requests() -> None:
    r = TriggerRegistry()
    r.request_execution(TriggerDefinition(trigger_id="t1", trigger_type="event"))
    r.request_execution(TriggerDefinition(trigger_id="t2", trigger_type="schedule"))
    pending = r.pending_requests()
    assert len(pending) == 2
    assert r.request_count == 0
