from runtime.api.knowledge import KnowledgeAPI


def _make_api() -> KnowledgeAPI:
    from runtime.kernel.lifecycle import LifecycleManager
    from runtime.services.events import EventBus
    from runtime.services.health import HealthService
    from runtime.services.manager import ServiceManager
    from runtime.services.registry import ServiceRegistry
    from runtime.services.resolver import DependencyResolver
    m = ServiceManager(registry=ServiceRegistry(), resolver=DependencyResolver(), lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus())
    return KnowledgeAPI(m)


def test_add_and_get() -> None:
    api = _make_api()
    e = api.add("k-1", "note", "Hello")
    assert e.entry_id == "k-1"
    assert api.get("k-1") is e


def test_get_missing() -> None:
    api = _make_api()
    assert api.get("missing") is None


def test_search_all() -> None:
    api = _make_api()
    api.add("a", "note", "A")
    api.add("b", "doc", "B")
    assert len(api.search()) == 2


def test_search_by_kind() -> None:
    api = _make_api()
    api.add("a", "note", "A")
    api.add("b", "doc", "B")
    assert len(api.search(kind="note")) == 1


def test_search_by_query() -> None:
    api = _make_api()
    api.add("a", "note", "Important note")
    api.add("b", "note", "Other")
    assert len(api.search(query="important")) == 1


def test_register_source() -> None:
    api = _make_api()
    s = api.register_source("src-1", "Doc Source")
    assert s.source_id == "src-1"
    assert s.name == "Doc Source"


def test_sources() -> None:
    api = _make_api()
    api.register_source("s1", "S1")
    api.register_source("s2", "S2")
    assert len(api.sources()) == 2


def test_index() -> None:
    api = _make_api()
    api.add("k-1", "note", "content")
    indexed = api.index("k-1")
    assert indexed is not None
    assert indexed.indexed_at is not None


def test_index_missing() -> None:
    api = _make_api()
    assert api.index("missing") is None


def test_remove() -> None:
    api = _make_api()
    api.add("x", "note", "X")
    assert api.remove("x") is True
    assert api.count() == 0


def test_remove_missing() -> None:
    api = _make_api()
    assert api.remove("missing") is False


def test_count() -> None:
    api = _make_api()
    api.add("a", "note", "A")
    api.add("b", "doc", "B")
    assert api.count() == 2
    assert api.count(kind="note") == 1


def test_shutdown_clears() -> None:
    api = _make_api()
    api.add("a", "note", "A")
    api.shutdown()
    assert api.count() == 0
