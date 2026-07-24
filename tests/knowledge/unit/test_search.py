from runtime.knowledge.catalog import KnowledgeCatalog
from runtime.knowledge.model import KnowledgeMetadata
from runtime.knowledge.search import KnowledgeSearch


def test_search() -> None:
    c = KnowledgeCatalog()
    c.index(KnowledgeMetadata(knowledge_id="k-1", title="API Reference", kind="doc", description="REST API docs", tags=("api",)))
    c.index(KnowledgeMetadata(knowledge_id="k-2", title="Architecture", kind="guide", description="System design"))
    s = KnowledgeSearch(c)
    assert len(s.search("api")) == 1
    assert len(s.search("guide")) == 0


def test_search_by_tag() -> None:
    c = KnowledgeCatalog()
    c.index(KnowledgeMetadata(knowledge_id="k-1", title="Test", kind="doc", tags=("core",)))
    s = KnowledgeSearch(c)
    assert len(s.search_by_tag("core")) == 1
    assert len(s.search_by_tag("missing")) == 0


def test_search_by_kind() -> None:
    c = KnowledgeCatalog()
    c.index(KnowledgeMetadata(knowledge_id="k-1", title="A", kind="doc"))
    c.index(KnowledgeMetadata(knowledge_id="k-2", title="B", kind="guide"))
    s = KnowledgeSearch(c)
    assert len(s.search_by_kind("doc")) == 1
