from runtime.assets.catalog import AssetCatalog
from runtime.assets.metadata import AssetMetadata


def test_index_and_get() -> None:
    c = AssetCatalog()
    m = AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0")
    c.index(m)
    entry = c.get("ast-1")
    assert entry is not None
    assert entry["asset_id"] == "ast-1"


def test_remove() -> None:
    c = AssetCatalog()
    m = AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0")
    c.index(m)
    assert c.remove("ast-1") is True
    assert c.count == 0


def test_filter_by_type() -> None:
    c = AssetCatalog()
    c.index(AssetMetadata(asset_id="a", asset_type="schema", version="1.0.0"))
    c.index(AssetMetadata(asset_id="b", asset_type="template", version="1.0.0"))
    assert len(c.filter(asset_type="schema")) == 1


def test_filter_by_owner() -> None:
    c = AssetCatalog()
    c.index(AssetMetadata(asset_id="a", asset_type="schema", version="1.0.0", owner="alice"))
    c.index(AssetMetadata(asset_id="b", asset_type="schema", version="1.0.0", owner="bob"))
    assert len(c.filter(owner="alice")) == 1


def test_filter_by_tag() -> None:
    c = AssetCatalog()
    c.index(AssetMetadata(asset_id="a", asset_type="schema", version="1.0.0", tags=("core",)))
    c.index(AssetMetadata(asset_id="b", asset_type="schema", version="1.0.0", tags=("draft",)))
    assert len(c.filter(tag="core")) == 1
