from runtime.knowledge.ingestion import KnowledgeIngestion
from runtime.knowledge.model import KnowledgeItem, KnowledgeSource


def test_ingest() -> None:
    ing = KnowledgeIngestion()
    item = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    source = KnowledgeSource(source_id="s-1", source_type="asset", name="Schema")
    result = ing.ingest(item, source)
    assert result.source is not None
    assert result.source.source_id == "s-1"
    assert ing.is_ingested("k-1") is True


def test_ingest_from_asset() -> None:
    ing = KnowledgeIngestion()
    item = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    result = ing.ingest_from_asset(item, "ast-1", "schema")
    assert result.source is not None
    assert result.source.source_type == "asset"


def test_ingest_from_project() -> None:
    ing = KnowledgeIngestion()
    item = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    result = ing.ingest_from_project(item, "proj-1")
    assert result.source is not None
    assert result.source.source_type == "project"


def test_ingested_at() -> None:
    ing = KnowledgeIngestion()
    item = KnowledgeItem(knowledge_id="k-1", title="Test", kind="doc")
    source = KnowledgeSource(source_id="s-1", source_type="asset", name="Schema")
    ing.ingest(item, source)
    assert ing.ingested_at("k-1") is not None
