from runtime.knowledge.model import (
    KnowledgeItem,
    KnowledgeMetadata,
    KnowledgeReference,
    KnowledgeSource,
)


def test_item_creation() -> None:
    i = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    assert i.knowledge_id == "k-1"
    assert i.kind == "doc"


def test_metadata() -> None:
    m = KnowledgeMetadata(knowledge_id="k-1", title="Test", kind="doc", version="1.0.0")
    assert m.version == "1.0.0"


def test_source() -> None:
    s = KnowledgeSource(source_id="s-1", source_type="asset", name="Schema")
    assert s.source_type == "asset"


def test_reference() -> None:
    r = KnowledgeReference(ref_id="r-1", ref_type="asset")
    assert r.ref_type == "asset"
