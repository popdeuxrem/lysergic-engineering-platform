from runtime.api.projects import ProjectAPI


def _make_api() -> ProjectAPI:
    from runtime.kernel.lifecycle import LifecycleManager
    from runtime.services.events import EventBus
    from runtime.services.health import HealthService
    from runtime.services.manager import ServiceManager
    from runtime.services.registry import ServiceRegistry
    from runtime.services.resolver import DependencyResolver
    m = ServiceManager(registry=ServiceRegistry(), resolver=DependencyResolver(), lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus())
    return ProjectAPI(m)


def test_create() -> None:
    api = _make_api()
    p = api.create("p-1", "Project 1")
    assert p.project_id == "p-1"
    assert p.name == "Project 1"


def test_get() -> None:
    api = _make_api()
    p = api.create("p-1", "P1")
    assert api.get("p-1") is p
    assert api.get("missing") is None


def test_list() -> None:
    api = _make_api()
    api.create("a", "A")
    api.create("b", "B")
    assert len(api.list()) == 2


def test_search() -> None:
    api = _make_api()
    api.create("a", "Alpha", description="first project")
    api.create("b", "Beta", description="second")
    assert len(api.search("alpha")) == 1
    assert len(api.search("project")) == 1
    assert len(api.search("x")) == 0


def test_update() -> None:
    api = _make_api()
    api.create("p-1", "Original")
    updated = api.update("p-1", name="Updated", description="new desc")
    assert updated is not None
    assert updated.name == "Updated"
    assert updated.description == "new desc"


def test_update_missing() -> None:
    api = _make_api()
    assert api.update("missing", name="X") is None


def test_remove() -> None:
    api = _make_api()
    api.create("x", "X")
    assert api.remove("x") is True
    assert api.count() == 0


def test_remove_missing() -> None:
    api = _make_api()
    assert api.remove("missing") is False


def test_count() -> None:
    api = _make_api()
    assert api.count() == 0
    api.create("a", "A")
    assert api.count() == 1


def test_shutdown_clears() -> None:
    api = _make_api()
    api.create("a", "A")
    api.shutdown()
    assert api.count() == 0
