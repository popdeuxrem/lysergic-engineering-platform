from runtime.automation.scheduler import Scheduler


def test_register_schedule() -> None:
    s = Scheduler()
    entry = s.register("sched-1", "a-1", interval_seconds=3600)
    assert entry.automation_id == "a-1"
    assert s.count == 1


def test_remove_schedule() -> None:
    s = Scheduler()
    s.register("sched-1", "a-1")
    assert s.remove("sched-1") is True
    assert s.count == 0


def test_due_automations() -> None:
    s = Scheduler()
    s.register("sched-1", "a-1", interval_seconds=0)
    entry = s.entries[0]
    entry.next_run = None
    assert len(s.due_automations()) == 0


def test_mark_run() -> None:
    s = Scheduler()
    s.register("sched-1", "a-1", interval_seconds=3600)
    s.mark_run("sched-1")
    entry = s.entries[0]
    assert entry.last_run is not None
