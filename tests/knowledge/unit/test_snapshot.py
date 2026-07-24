from runtime.knowledge.model import KnowledgeItem
from runtime.knowledge.snapshot import KnowledgeSnapshot


def test_snapshot() -> None:
    i = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    snap = KnowledgeSnapshot(items={"k-1": i}, version=1)
    assert snap.count() == 1
    assert snap.get("k-1") is i


def test_list() -> None:
    items = {"a": KnowledgeItem(knowledge_id="a", title="A", kind="doc"), "b": KnowledgeItem(knowledge_id="b", title="B", kind="doc")}
    snap = KnowledgeSnapshot(items=items, version=2)
    assert len(snap.list()) == 2


def test_version() -> None:
    snap = KnowledgeSnapshot(items={}, version=5)
    assert snap.version == 5


def test_to_dict() -> None:
    snap = KnowledgeSnapshot(items={}, version=1)
    d = snap.to_dict()
    assert d["version"] == 1
