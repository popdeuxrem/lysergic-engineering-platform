from runtime.assets.metadata import AssetMetadata


def test_metadata_creation() -> None:
    m = AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0")
    assert m.asset_id == "ast-1"
    assert m.asset_type == "schema"
    assert m.version == "1.0.0"


def test_metadata_defaults() -> None:
    m = AssetMetadata(asset_id="a", asset_type="t", version="0.1.0")
    assert m.owner == ""
    assert m.tags == ()
    assert m.description == ""


def test_metadata_with_tags() -> None:
    m = AssetMetadata(asset_id="a", asset_type="t", version="1.0.0", tags=("core", "stable"))
    assert "core" in m.tags
    assert len(m.tags) == 2


def test_metadata_to_dict() -> None:
    m = AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0", owner="team")
    d = m.to_dict()
    assert d["asset_id"] == "ast-1"
    assert d["owner"] == "team"
    assert d["version"] == "1.0.0"
