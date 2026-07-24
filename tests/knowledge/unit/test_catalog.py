from runtime.knowledge.catalog import KnowledgeCatalog
from runtime.knowledge.model import KnowledgeMetadata


def test_index_and_get() -> None:
    c = KnowledgeCatalog()
    m = KnowledgeMetadata(knowledge_id="k-1", title="Test", kind="doc")
    c.index(m)
    entry = c.get("k-1")
    assert entry is not None and entry["title"] == "Test"


def test_remove() -> None:
    c = KnowledgeCatalog()
    c.index(KnowledgeMetadata(knowledge_id="k-1", title="T", kind="doc"))
    assert c.remove("k-1") is True
    assert c.count == 0


def test_filter_by_kind() -> None:
    c = KnowledgeCatalog()
    c.index(KnowledgeMetadata(knowledge_id="a", title="A", kind="doc"))
    c.index(KnowledgeMetadata(knowledge_id="b", title="B", kind="guide"))
    assert len(c.filter(kind="doc")) == 1


def test_filter_by_tag() -> None:
    c = KnowledgeCatalog()
    c.index(KnowledgeMetadata(knowledge_id="a", title="A", kind="doc", tags=("core",)))
    assert len(c.filter(tag="core")) == 1
