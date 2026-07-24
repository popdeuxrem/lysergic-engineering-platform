from runtime.api.workflows import WorkflowAPI, WorkflowStatus
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceRegistry
from runtime.services.resolver import DependencyResolver


def _make_manager() -> ServiceManager:
    return ServiceManager(
        registry=ServiceRegistry(),
        resolver=DependencyResolver(),
        lifecycle=LifecycleManager(),
        health=HealthService(),
        event_bus=EventBus(),
    )


def test_workflow_create_and_get() -> None:
    api = WorkflowAPI(_make_manager())
    wf = api.create("wf-1", "Test Workflow")
    assert wf.workflow_id == "wf-1"
    assert wf.status == WorkflowStatus.PENDING
    assert api.get("wf-1") is wf


def test_workflow_get_missing() -> None:
    api = WorkflowAPI(_make_manager())
    assert api.get("nonexistent") is None


def test_workflow_list_all() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("a", "A")
    api.create("b", "B")
    assert len(api.list()) == 2


def test_workflow_list_by_status() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("a", "A")
    api.create("b", "B")
    api.start("a")
    pending = api.list(status=WorkflowStatus.PENDING)
    running = api.list(status=WorkflowStatus.RUNNING)
    assert len(pending) == 1
    assert len(running) == 1


def test_workflow_start() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("w", "W")
    result = api.start("w")
    assert result is not None
    assert result.status == WorkflowStatus.RUNNING


def test_workflow_start_non_pending() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("w", "W")
    api.start("w")
    assert api.start("w") is None


def test_workflow_complete() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("w", "W", steps=("a", "b"))
    api.start("w")
    result = api.complete("w")
    assert result is not None
    assert result.status == WorkflowStatus.COMPLETED
    assert result.current_step == 2


def test_workflow_complete_non_running() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("w", "W")
    assert api.complete("w") is None


def test_workflow_fail() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("w", "W")
    api.start("w")
    result = api.fail("w", "Something broke")
    assert result is not None
    assert result.status == WorkflowStatus.FAILED
    assert result.error == "Something broke"


def test_workflow_cancel() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("w", "W")
    result = api.cancel("w")
    assert result is not None
    assert result.status == WorkflowStatus.CANCELLED


def test_workflow_cancel_running() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("w", "W")
    api.start("w")
    result = api.cancel("w")
    assert result is not None
    assert result.status == WorkflowStatus.CANCELLED


def test_workflow_state_transitions_missing() -> None:
    api = WorkflowAPI(_make_manager())
    assert api.start("missing") is None
    assert api.complete("missing") is None
    assert api.fail("missing", "err") is None
    assert api.cancel("missing") is None


def test_workflow_count() -> None:
    api = WorkflowAPI(_make_manager())
    assert api.count() == 0
    api.create("a", "A")
    assert api.count() == 1


def test_workflow_shutdown_clears() -> None:
    api = WorkflowAPI(_make_manager())
    api.create("w", "W")
    api.shutdown()
    assert api.count() == 0
