from runtime.assets.metadata import AssetMetadata
from runtime.assets.registry import AssetEntry, AssetRegistry


def test_register() -> None:
    r = AssetRegistry()
    entry = AssetEntry(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    r.register(entry)
    assert "ast-1" in r
    assert r.count == 1


def test_register_duplicate_raises() -> None:
    r = AssetRegistry()
    r.register(AssetEntry(AssetMetadata(asset_id="a", asset_type="t", version="1.0.0")))
    try:
        r.register(AssetEntry(AssetMetadata(asset_id="a", asset_type="t", version="1.0.0")))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_get() -> None:
    r = AssetRegistry()
    entry = AssetEntry(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    r.register(entry)
    assert r.get("ast-1") is entry
    assert r.get("missing") is None


def test_get_by_type() -> None:
    r = AssetRegistry()
    r.register(AssetEntry(AssetMetadata(asset_id="a", asset_type="schema", version="1.0.0")))
    r.register(AssetEntry(AssetMetadata(asset_id="b", asset_type="schema", version="2.0.0")))
    r.register(AssetEntry(AssetMetadata(asset_id="c", asset_type="template", version="1.0.0")))
    assert len(r.get_by_type("schema")) == 2
    assert len(r.get_by_type("template")) == 1


def test_get_by_version() -> None:
    r = AssetRegistry()
    r.register(AssetEntry(AssetMetadata(asset_id="a", asset_type="schema", version="1.0.0")))
    r.register(AssetEntry(AssetMetadata(asset_id="b", asset_type="schema", version="2.0.0")))
    assert len(r.get_by_version("schema", "1.0.0")) == 1


def test_remove() -> None:
    r = AssetRegistry()
    r.register(AssetEntry(AssetMetadata(asset_id="a", asset_type="t", version="1.0.0")))
    assert r.remove("a") is True
    assert r.count == 0


def test_freeze() -> None:
    r = AssetRegistry()
    r.freeze()
    try:
        r.register(AssetEntry(AssetMetadata(asset_id="late", asset_type="t", version="1.0.0")))
        assert False
    except Exception:  # noqa: BLE001, S110
        pass
