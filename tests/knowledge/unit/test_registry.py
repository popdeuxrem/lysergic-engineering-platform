from runtime.knowledge.model import KnowledgeItem
from runtime.knowledge.registry import KnowledgeRegistry


def test_register() -> None:
    r = KnowledgeRegistry()
    r.register(KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc"))
    assert "k-1" in r
    assert r.count == 1


def test_duplicate_raises() -> None:
    r = KnowledgeRegistry()
    r.register(KnowledgeItem(knowledge_id="k-1", title="T", kind="doc"))
    try:
        r.register(KnowledgeItem(knowledge_id="k-1", title="T", kind="doc"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_get() -> None:
    r = KnowledgeRegistry()
    i = KnowledgeItem(knowledge_id="k-1", title="T", kind="doc")
    r.register(i)
    assert r.get("k-1") is i
    assert r.get("missing") is None


def test_unregister() -> None:
    r = KnowledgeRegistry()
    r.register(KnowledgeItem(knowledge_id="a", title="A", kind="doc"))
    assert r.unregister("a") is True
    assert r.count == 0


def test_list() -> None:
    r = KnowledgeRegistry()
    r.register(KnowledgeItem(knowledge_id="a", title="A", kind="doc"))
    r.register(KnowledgeItem(knowledge_id="b", title="B", kind="guide"))
    assert len(r.list()) == 2


def test_list_by_kind() -> None:
    r = KnowledgeRegistry()
    r.register(KnowledgeItem(knowledge_id="a", title="A", kind="doc"))
    r.register(KnowledgeItem(knowledge_id="b", title="B", kind="doc"))
    r.register(KnowledgeItem(knowledge_id="c", title="C", kind="guide"))
    assert len(r.list_by_kind("doc")) == 2


def test_list_by_tag() -> None:
    r = KnowledgeRegistry()
    r.register(KnowledgeItem(knowledge_id="a", title="A", kind="doc", tags=("core",)))
    r.register(KnowledgeItem(knowledge_id="b", title="B", kind="doc", tags=("draft",)))
    assert len(r.list_by_tag("core")) == 1


def test_freeze() -> None:
    r = KnowledgeRegistry()
    r.freeze()
    try:
        r.register(KnowledgeItem(knowledge_id="late", title="Late", kind="doc"))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass
