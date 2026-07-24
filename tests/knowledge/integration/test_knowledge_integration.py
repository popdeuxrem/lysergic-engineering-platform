from runtime.knowledge.manager import KnowledgeManager
from runtime.knowledge.model import KnowledgeSource
from runtime.services.events import EventBus


def test_full_lifecycle() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))

    m = KnowledgeManager(event_bus=bus)
    m.initialize_runtime()

    m.create("k-1", "Knowledge Base", "doc")
    assert "knowledge.KnowledgeCreated" in events

    source = KnowledgeSource(source_id="s-1", source_type="asset", name="Schema")
    m.ingest("k-1", source)
    assert "knowledge.KnowledgeIngested" in events
    assert m.status("k-1") == "ingested"

    m.validate_item("k-1")
    assert "knowledge.KnowledgeValidated" in events
    assert m.status("k-1") == "validated"

    m.publish("k-1")
    assert "knowledge.KnowledgePublished" in events
    assert m.status("k-1") == "available"

    m.deprecate("k-1")
    assert "knowledge.KnowledgeDeprecated" in events
    assert m.status("k-1") == "deprecated"

    m.archive_item("k-1")
    assert "knowledge.KnowledgeArchived" in events
    assert m.status("k-1") == "archived"


def test_provenance_tracking() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Design Doc", "doc", author="alice")

    source = KnowledgeSource(source_id="ast-1", source_type="asset", name="Schema")
    m.ingest("k-1", source)

    prov = m.provenance_of("k-1")
    assert prov is not None
    assert prov["origin"] == "direct_creation"
    assert prov["source"] is not None


def test_search_functionality() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Getting Started", "guide", description="Quick start guide", tags=("beginner",))
    m.create("k-2", "API Reference", "doc", description="Complete API docs", tags=("advanced",))

    assert len(m.search_items("guide")) == 1
    assert len(m.search_items("api")) == 1
    assert len(m.search_items("started")) == 1
