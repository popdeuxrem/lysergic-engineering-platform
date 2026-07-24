from runtime.configuration import (
    ConfigSnapshot,
    ConfigurationManager,
    ProfileDefinition,
)
from runtime.services.events import EventBus


def test_full_lifecycle() -> None:
    bus = EventBus()
    events: list[str] = []
    bus.subscribe_all(lambda e: events.append(e.event_type))

    m = ConfigurationManager(event_bus=bus)
    m.profile_manager.define(ProfileDefinition(profile_id="prod", name="Production", config={"env": "prod"}))
    m.profile_manager.activate("prod")
    m.initialize()

    assert m.snapshot is not None
    assert m.get("platform.name") == "Lysergic Engineering Platform"
    assert m.get("env") == "prod"
    assert "config.initialized" in events

    m.set_override("feature.flag", True)
    assert m.get("feature.flag") is True

    m.shutdown()
    assert "config.stopped" in events
    assert m.snapshot is None


def test_layered_resolution() -> None:
    m = ConfigurationManager()
    m.profile_manager.define(ProfileDefinition(profile_id="dev", name="Dev", config={"key": "profile"}))
    m.profile_manager.activate("dev")
    m.initialize()

    assert m.get("key") == "profile"

    m.set_override("key", "override")
    assert m.get("key") == "override"


def test_snapshot_immutability() -> None:
    m = ConfigurationManager()
    m.initialize()
    snap = m.snapshot
    assert snap is not None
    assert isinstance(snap, ConfigSnapshot)
    assert snap.frozen is True
