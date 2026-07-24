from runtime.assets.manager import AssetManager
from runtime.assets.metadata import AssetMetadata


def test_initial_state() -> None:
    m = AssetManager()
    assert m.status.name == "PENDING"


def test_initialize() -> None:
    m = AssetManager()
    m.initialize()
    assert m.status.name == "READY"


def test_register() -> None:
    m = AssetManager()
    m.initialize()
    meta = AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0")
    entry = m.register(meta)
    assert entry.metadata.asset_id == "ast-1"
    assert m.get("ast-1") is not None


def test_get_missing() -> None:
    m = AssetManager()
    m.initialize()
    assert m.get("missing") is None


def test_list() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="a", asset_type="schema", version="1.0.0"))
    m.register(AssetMetadata(asset_id="b", asset_type="template", version="1.0.0"))
    assert len(m.list()) == 2
    assert len(m.list(asset_type="schema")) == 1


def test_validate() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    m.validate("ast-1")
    state = m.lifecycle.state_of("ast-1")
    assert state is not None and state.value == "validated"


def test_activate() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    m.validate("ast-1")
    m.activate("ast-1")
    state = m.lifecycle.state_of("ast-1")
    assert state is not None and state.value == "available"


def test_deprecate() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    m.validate("ast-1")
    m.activate("ast-1")
    m.deprecate("ast-1")
    state = m.lifecycle.state_of("ast-1")
    assert state is not None and state.value == "deprecated"


def test_remove() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    assert m.remove("ast-1") is True
    assert m.get("ast-1") is None


def test_remove_missing() -> None:
    m = AssetManager()
    m.initialize()
    assert m.remove("missing") is False


def test_search() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="my-asset", asset_type="schema", version="1.0.0", description="important"))
    results = m.search_assets("important")
    assert len(results) == 1
    results = m.search_assets("nope")
    assert len(results) == 0


def test_snapshot() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    snap = m.snapshot_state()
    assert snap.count() == 1
    assert snap.get("ast-1") is not None


def test_shutdown() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    m.shutdown()
    assert m.get("ast-1") is None
