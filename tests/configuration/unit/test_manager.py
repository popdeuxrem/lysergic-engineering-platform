from runtime.configuration.manager import ConfigurationManager
from runtime.services.events import EventBus


def test_initial_state() -> None:
    m = ConfigurationManager()
    assert m.snapshot is None
    assert m.status.name == "PENDING"


def test_initialize() -> None:
    m = ConfigurationManager()
    m.initialize()
    assert m.snapshot is not None
    assert m.status.name == "READY"


def test_initialize_idempotent() -> None:
    m = ConfigurationManager()
    m.initialize()
    v1 = m.snapshot.version if m.snapshot else -1
    m.initialize()
    v2 = m.snapshot.version if m.snapshot else -1
    assert v1 == v2


def test_get_after_initialize() -> None:
    m = ConfigurationManager()
    m.initialize()
    assert m.get("platform.name") == "Lysergic Engineering Platform"
    assert m.get("nonexistent", "fallback") == "fallback"
    assert m.get("nonexistent") is None


def test_has() -> None:
    m = ConfigurationManager()
    m.initialize()
    assert m.has("platform.name") is True
    assert m.has("nonexistent") is False


def test_all() -> None:
    m = ConfigurationManager()
    m.initialize()
    result = m.all()
    assert "platform" in result
    assert "validation" in result


def test_set_override() -> None:
    m = ConfigurationManager()
    m.initialize()
    m.set_override("platform.name", "Override")
    assert m.get("platform.name") == "Override"


def test_resolve_with_source() -> None:
    m = ConfigurationManager()
    m.initialize()
    resolved = m.resolve_with_source()
    assert "platform" in resolved
    key, _source = resolved["platform"]
    assert isinstance(key, dict) and key.get("name") == "Lysergic Engineering Platform"


def test_shutdown() -> None:
    m = ConfigurationManager()
    m.initialize()
    m.shutdown()
    assert m.snapshot is None
    assert m.status.name == "PENDING"


def test_event_publishing() -> None:
    bus = EventBus()
    received: list[str] = []
    bus.subscribe("config.initialized", lambda e: received.append(e.event_type))
    m = ConfigurationManager(event_bus=bus)
    m.initialize()
    assert "config.initialized" in received
