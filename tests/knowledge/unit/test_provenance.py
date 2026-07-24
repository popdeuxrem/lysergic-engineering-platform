from runtime.knowledge.model import KnowledgeItem
from runtime.knowledge.provenance import ProvenanceTracker


def test_record() -> None:
    t = ProvenanceTracker()
    item = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    record = t.record(item, origin="test", creator="alice")
    assert record.knowledge_id == "k-1"
    assert record.origin == "test"
    assert record.creator == "alice"


def test_add_transformation() -> None:
    t = ProvenanceTracker()
    item = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    t.record(item, origin="test")
    t.add_transformation("k-1", "validated")
    record = t.get("k-1")
    assert record is not None and "validated" in record.transformations


def test_add_relationship() -> None:
    t = ProvenanceTracker()
    item = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    t.record(item, origin="test")
    t.add_relationship("k-1", "derived_from:ast-1")
    record = t.get("k-1")
    assert record is not None and "derived_from:ast-1" in record.relationships


def test_get_missing() -> None:
    t = ProvenanceTracker()
    assert t.get("missing") is None


def test_to_dict() -> None:
    t = ProvenanceTracker()
    item = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    t.record(item, origin="test")
    record = t.get("k-1")
    d = record.to_dict()
    assert d["knowledge_id"] == "k-1"
    assert d["origin"] == "test"
