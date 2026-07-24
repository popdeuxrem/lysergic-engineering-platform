from datetime import UTC, datetime, timedelta

from runtime.api.workflows import WorkflowAPI, WorkflowStatus


def _make_api() -> WorkflowAPI:
    from runtime.kernel.lifecycle import LifecycleManager
    from runtime.services.events import EventBus
    from runtime.services.health import HealthService
    from runtime.services.manager import ServiceManager
    from runtime.services.registry import ServiceRegistry
    from runtime.services.resolver import DependencyResolver
    m = ServiceManager(registry=ServiceRegistry(), resolver=DependencyResolver(), lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus())
    return WorkflowAPI(m)


def test_create() -> None:
    api = _make_api()
    w = api.create("wf-1", "Test")
    assert w.workflow_id == "wf-1"
    assert w.status == WorkflowStatus.PENDING


def test_get() -> None:
    api = _make_api()
    w = api.create("wf-1", "T")
    assert api.get("wf-1") is w
    assert api.get("missing") is None


def test_list_all() -> None:
    api = _make_api()
    api.create("a", "A")
    api.create("b", "B")
    assert len(api.list()) == 2


def test_list_by_status() -> None:
    api = _make_api()
    api.create("a", "A")
    api.create("b", "B")
    api.start("a")
    assert len(api.list(WorkflowStatus.RUNNING)) == 1
    assert len(api.list(WorkflowStatus.PENDING)) == 1


def test_start() -> None:
    api = _make_api()
    api.create("w", "W")
    r = api.start("w")
    assert r is not None and r.status == WorkflowStatus.RUNNING


def test_start_non_startable() -> None:
    api = _make_api()
    api.create("w", "W")
    api.start("w")
    assert api.start("w") is None


def test_complete() -> None:
    api = _make_api()
    api.create("w", "W", steps=("a",))
    api.start("w")
    r = api.complete("w")
    assert r is not None and r.status == WorkflowStatus.COMPLETED


def test_fail() -> None:
    api = _make_api()
    api.create("w", "W")
    api.start("w")
    r = api.fail("w", "error")
    assert r is not None and r.status == WorkflowStatus.FAILED


def test_cancel() -> None:
    api = _make_api()
    api.create("w", "W")
    r = api.cancel("w")
    assert r is not None and r.status == WorkflowStatus.CANCELLED


def test_schedule() -> None:
    api = _make_api()
    api.create("w", "W")
    future = datetime.now(UTC) + timedelta(hours=1)
    r = api.schedule("w", future)
    assert r is not None and r.status == WorkflowStatus.SCHEDULED


def test_schedule_non_pending() -> None:
    api = _make_api()
    api.create("w", "W")
    api.start("w")
    assert api.schedule("w", datetime.now(UTC)) is None


def test_history() -> None:
    api = _make_api()
    api.create("w", "W")
    api.start("w")
    api.complete("w")
    assert len(api.history()) == 1


def test_list_scheduled() -> None:
    api = _make_api()
    api.create("a", "A")
    api.create("b", "B")
    api.schedule("a", datetime.now(UTC) + timedelta(hours=1))
    assert len(api.list_scheduled()) == 1


def test_count() -> None:
    api = _make_api()
    api.create("a", "A")
    assert api.count() == 1


def test_shutdown_clears() -> None:
    api = _make_api()
    api.create("w", "W")
    api.shutdown()
    assert api.count() == 0
