from runtime.api.knowledge import KnowledgeAPI
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


def test_knowledge_add_and_get() -> None:
    api = KnowledgeAPI(_make_manager())
    entry = api.add("k-1", "note", "Hello world")
    assert entry.entry_id == "k-1"
    assert entry.content == "Hello world"
    assert api.get("k-1") is entry


def test_knowledge_get_missing() -> None:
    api = KnowledgeAPI(_make_manager())
    assert api.get("nonexistent") is None


def test_knowledge_search_all() -> None:
    api = KnowledgeAPI(_make_manager())
    api.add("a", "note", "Content A")
    api.add("b", "doc", "Content B")
    assert len(api.search()) == 2


def test_knowledge_search_by_kind() -> None:
    api = KnowledgeAPI(_make_manager())
    api.add("a", "note", "Note A")
    api.add("b", "note", "Note B")
    api.add("c", "doc", "Doc C")
    assert len(api.search(kind="note")) == 2
    assert len(api.search(kind="doc")) == 1


def test_knowledge_search_by_tag() -> None:
    api = KnowledgeAPI(_make_manager())
    api.add("a", "note", "A", tags=("important",))
    api.add("b", "note", "B", tags=("draft",))
    assert len(api.search(tag="important")) == 1
    assert len(api.search(tag="draft")) == 1
    assert len(api.search(tag="nonexistent")) == 0


def test_knowledge_remove() -> None:
    api = KnowledgeAPI(_make_manager())
    api.add("x", "note", "X")
    assert api.remove("x") is True
    assert api.count() == 0


def test_knowledge_remove_missing() -> None:
    api = KnowledgeAPI(_make_manager())
    assert api.remove("nonexistent") is False


def test_knowledge_count_all() -> None:
    api = KnowledgeAPI(_make_manager())
    api.add("a", "note", "A")
    api.add("b", "doc", "B")
    assert api.count() == 2


def test_knowledge_count_by_kind() -> None:
    api = KnowledgeAPI(_make_manager())
    api.add("a", "note", "A")
    api.add("b", "note", "B")
    api.add("c", "doc", "C")
    assert api.count(kind="note") == 2
    assert api.count(kind="doc") == 1


def test_knowledge_shutdown_clears() -> None:
    api = KnowledgeAPI(_make_manager())
    api.add("a", "note", "A")
    api.shutdown()
    assert api.count() == 0
