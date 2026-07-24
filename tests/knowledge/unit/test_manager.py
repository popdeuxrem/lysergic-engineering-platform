from runtime.knowledge.manager import KnowledgeManager
from runtime.knowledge.model import KnowledgeSource
from runtime.services.events import EventBus


def test_initial_state() -> None:
    m = KnowledgeManager()
    assert m.manager_status.name == "PENDING"


def test_initialize() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    assert m.manager_status.name == "READY"


def test_create() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    item = m.create("k-1", "Test", "doc", "content")
    assert item.knowledge_id == "k-1"
    assert m.get("k-1") is not None


def test_get_missing() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    assert m.get("missing") is None


def test_list() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("a", "A", "doc")
    m.create("b", "B", "guide")
    assert len(m.list()) == 2


def test_ingest() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    source = KnowledgeSource(source_id="s-1", source_type="asset", name="Schema")
    result = m.ingest("k-1", source)
    assert result is not None
    assert m.status("k-1") == "ingested"


def test_validate_item() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    source = KnowledgeSource(source_id="s-1", source_type="asset", name="S")
    m.ingest("k-1", source)
    m.validate_item("k-1")
    assert m.status("k-1") == "validated"


def test_publish() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    source = KnowledgeSource(source_id="s-1", source_type="asset", name="S")
    m.ingest("k-1", source)
    m.validate_item("k-1")
    m.publish("k-1")
    assert m.status("k-1") == "available"


def test_deprecate() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    source = KnowledgeSource(source_id="s-1", source_type="asset", name="S")
    m.ingest("k-1", source)
    m.validate_item("k-1")
    m.publish("k-1")
    m.deprecate("k-1")
    assert m.status("k-1") == "deprecated"


def test_archive_item() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    m.archive_item("k-1")
    assert m.status("k-1") == "archived"


def test_remove() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    assert m.remove("k-1") is True
    assert m.get("k-1") is None


def test_search() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "API Reference", "doc", description="REST API docs")
    results = m.search_items("API")
    assert len(results) == 1


def test_provenance() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    prov = m.provenance_of("k-1")
    assert prov is not None
    assert prov["origin"] == "direct_creation"


def test_status() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    assert m.status("k-1") == "created"
    assert m.status("missing") is None


def test_snapshot() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    snap = m.snapshot_state()
    assert snap.count() == 1


def test_events() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))
    m = KnowledgeManager(event_bus=bus)
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    assert "knowledge.KnowledgeCreated" in events


def test_shutdown() -> None:
    m = KnowledgeManager()
    m.initialize_runtime()
    m.create("k-1", "Test", "doc")
    m.shutdown()
    assert m.get("k-1") is None
