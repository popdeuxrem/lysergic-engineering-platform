from runtime.api.projects import ProjectAPI
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


def test_project_create_and_get() -> None:
    api = ProjectAPI(_make_manager())
    manifest = api.create("proj-1", "Test Project")
    assert manifest.project_id == "proj-1"
    assert manifest.name == "Test Project"
    assert api.get("proj-1") is manifest


def test_project_get_missing() -> None:
    api = ProjectAPI(_make_manager())
    assert api.get("nonexistent") is None


def test_project_list() -> None:
    api = ProjectAPI(_make_manager())
    api.create("a", "Project A")
    api.create("b", "Project B")
    assert len(api.list()) == 2


def test_project_remove() -> None:
    api = ProjectAPI(_make_manager())
    api.create("x", "To Remove")
    assert api.remove("x") is True
    assert api.count() == 0


def test_project_remove_missing() -> None:
    api = ProjectAPI(_make_manager())
    assert api.remove("nonexistent") is False


def test_project_count() -> None:
    api = ProjectAPI(_make_manager())
    assert api.count() == 0
    api.create("a", "A")
    assert api.count() == 1


def test_project_create_with_metadata() -> None:
    api = ProjectAPI(_make_manager())
    manifest = api.create("m", "Meta", description="test", metadata={"key": "val"})
    assert manifest.description == "test"
    assert manifest.metadata == {"key": "val"}


def test_project_shutdown_clears() -> None:
    api = ProjectAPI(_make_manager())
    api.create("a", "A")
    api.shutdown()
    assert api.count() == 0
