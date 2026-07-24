from runtime.knowledge.model import KnowledgeItem
from runtime.knowledge.validator import KnowledgeValidator


def test_validate_valid() -> None:
    v = KnowledgeValidator()
    i = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    result = v.validate_tier1(i)
    assert result.valid is True


def test_validate_missing_id() -> None:
    v = KnowledgeValidator()
    i = KnowledgeItem(knowledge_id="", title="Test", kind="doc")
    result = v.validate_tier1(i)
    assert result.valid is False


def test_validate_missing_title() -> None:
    v = KnowledgeValidator()
    i = KnowledgeItem(knowledge_id="k-1", title="", kind="doc")
    result = v.validate_tier1(i)
    assert result.valid is False


def test_validate_missing_kind() -> None:
    v = KnowledgeValidator()
    i = KnowledgeItem(knowledge_id="k-1", title="Test", kind="")
    result = v.validate_tier1(i)
    assert result.valid is False


def test_validate_tier2_duplicate_refs() -> None:
    from runtime.knowledge.model import KnowledgeReference
    v = KnowledgeValidator()
    refs = (KnowledgeReference(ref_id="r1", ref_type="asset"), KnowledgeReference(ref_id="r1", ref_type="asset"))
    i = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc", references=refs)
    result = v.validate_tier2(i)
    assert result.valid is False


def test_validate_tier2_ok() -> None:
    v = KnowledgeValidator()
    i = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    result = v.validate_tier2(i)
    assert result.valid is True
