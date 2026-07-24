from runtime.knowledge.exceptions import (
    IngestionError,
    InvalidLifecycleTransitionError,
    KnowledgeNotFoundError,
)


def test_not_found() -> None:
    e = KnowledgeNotFoundError("k-1")
    assert e.knowledge_id == "k-1"


def test_invalid_transition() -> None:
    e = InvalidLifecycleTransitionError("created", "available")
    assert e.current == "created"
    assert e.target == "available"


def test_ingestion_error() -> None:
    e = IngestionError("source-1", "failed")
    assert "source-1" in str(e)
