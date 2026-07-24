from runtime.assets.manager import AssetManager
from runtime.assets.metadata import AssetMetadata
from runtime.assets.snapshot import AssetSnapshot
from runtime.services.events import EventBus


def test_full_lifecycle() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))

    m = AssetManager(event_bus=bus)
    m.initialize()

    meta = AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0", owner="team")
    m.register(meta)
    assert "asset.AssetRegistered" in events

    m.validate("ast-1")
    state = m.lifecycle.state_of("ast-1")
    assert state is not None and state.value == "validated"

    m.activate("ast-1")
    state = m.lifecycle.state_of("ast-1")
    assert state is not None and state.value == "available"

    m.deprecate("ast-1")
    state = m.lifecycle.state_of("ast-1")
    assert state is not None and state.value == "deprecated"

    m.remove("ast-1")
    assert m.get("ast-1") is None
    assert "asset.AssetRemoved" in events


def test_snapshot_isolation() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="ast-1", asset_type="schema", version="1.0.0"))
    snap = m.snapshot_state()
    assert isinstance(snap, AssetSnapshot)
    assert snap.count() == 1
    assert snap.get("ast-1") is not None


def test_search_and_catalog() -> None:
    m = AssetManager()
    m.initialize()
    m.register(AssetMetadata(asset_id="doc-1", asset_type="document", version="1.0.0", description="API docs", tags=("docs",)))
    m.register(AssetMetadata(asset_id="schema-1", asset_type="schema", version="2.0.0", description="core schema", tags=("core",)))
    assert len(m.search_assets("docs")) == 1
    assert len(m.search_assets("schema")) == 1
    assert len(m.search_assets("api")) == 1


def test_multiple_assets() -> None:
    m = AssetManager()
    m.initialize()
    for i in range(5):
        m.register(AssetMetadata(asset_id=f"ast-{i}", asset_type="schema", version=f"{i}.0.0"))
    assert len(m.list()) == 5
