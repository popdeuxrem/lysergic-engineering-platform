from runtime.services.events import Event, EventBus


def test_event_creation() -> None:
    event = Event(event_type="test.event", payload={"key": "val"}, source="test")
    assert event.event_type == "test.event"
    assert event.payload == {"key": "val"}
    assert event.source == "test"


def test_event_to_dict() -> None:
    event = Event(event_type="e", source="s")
    d = event.to_dict()
    assert d["event_type"] == "e"
    assert d["source"] == "s"
    assert "timestamp" in d


def test_publish_and_subscribe() -> None:
    bus = EventBus()
    received: list[Event] = []

    def handler(event: Event) -> None:
        received.append(event)

    bus.subscribe("test.event", handler)
    bus.publish(Event(event_type="test.event"))
    assert len(received) == 1
    assert received[0].event_type == "test.event"


def test_wildcard_handler() -> None:
    bus = EventBus()
    received: list[Event] = []

    bus.subscribe_all(received.append)
    bus.publish(Event(event_type="a"))
    bus.publish(Event(event_type="b"))
    assert len(received) == 2


def test_unsubscribe() -> None:
    bus = EventBus()
    received: list[Event] = []

    def handler(event: Event) -> None:
        received.append(event)

    bus.subscribe("test.event", handler)
    bus.unsubscribe("test.event", handler)
    bus.publish(Event(event_type="test.event"))
    assert len(received) == 0


def test_history() -> None:
    bus = EventBus()
    bus.publish(Event(event_type="e1"))
    bus.publish(Event(event_type="e2"))
    assert len(bus.history) == 2
    assert bus.history[0].event_type == "e1"
    assert bus.history[1].event_type == "e2"


def test_clear_history() -> None:
    bus = EventBus()
    bus.publish(Event(event_type="e"))
    bus.clear()
    assert len(bus.history) == 0


def test_subscriber_count() -> None:
    bus = EventBus()
    assert bus.subscriber_count == 0
    bus.subscribe("a", lambda e: None)
    bus.subscribe("a", lambda e: None)
    bus.subscribe("b", lambda e: None)
    bus.subscribe_all(lambda e: None)
    assert bus.subscriber_count == 4
