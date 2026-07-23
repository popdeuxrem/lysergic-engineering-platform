from runtime.telemetry.interface import TelemetryEmitter, TelemetryEvent


class FakeTelemetryEmitter:
    def __init__(self) -> None:
        self.events: list[TelemetryEvent] = []
        self._enabled = True

    def emit(self, event: TelemetryEvent) -> None:
        self.events.append(event)

    @property
    def enabled(self) -> bool:
        return self._enabled


def test_telemetry_emitter_protocol_satisfied() -> None:
    emitter: TelemetryEmitter = FakeTelemetryEmitter()
    assert isinstance(emitter, TelemetryEmitter)


def test_telemetry_event_creation() -> None:
    event = TelemetryEvent(event_type="runtime.start", payload={"version": "0.1.0"}, source="kernel")
    assert event.event_type == "runtime.start"
    assert event.payload == {"version": "0.1.0"}
    assert event.source == "kernel"
    assert event.timestamp is not None


def test_telemetry_event_to_dict() -> None:
    event = TelemetryEvent(event_type="test.event", payload={"key": "value"}, source="test")
    d = event.to_dict()
    assert d["event_type"] == "test.event"
    assert d["payload"] == {"key": "value"}
    assert d["source"] == "test"
    assert "timestamp" in d


def test_emitter_collects_events() -> None:
    emitter = FakeTelemetryEmitter()
    event1 = TelemetryEvent(event_type="event.1")
    event2 = TelemetryEvent(event_type="event.2")
    emitter.emit(event1)
    emitter.emit(event2)
    assert len(emitter.events) == 2
    assert emitter.events[0].event_type == "event.1"
    assert emitter.events[1].event_type == "event.2"


def test_emitter_enabled_property() -> None:
    emitter = FakeTelemetryEmitter()
    assert emitter.enabled is True
