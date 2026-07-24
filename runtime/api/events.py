from __future__ import annotations

from typing import Any

from runtime.services.events import Event, EventBus as _EventBus

_EVENT_BUS: _EventBus | None = None


def _get_bus() -> _EventBus:
    global _EVENT_BUS
    if _EVENT_BUS is None:
        _EVENT_BUS = _EventBus()
    return _EVENT_BUS


def publish_event(event_type: str, payload: dict[str, Any] | None = None, source: str = "") -> None:
    bus = _get_bus()
    bus.publish(Event(event_type=event_type, payload=payload or {}, source=source))
