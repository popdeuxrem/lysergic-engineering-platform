from __future__ import annotations

from runtime.services.events import Event, EventBus


class ExtensionRuntimeEventPublisher:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus

    def installed(self, extension_id: str) -> None:
        self._publish("ExtensionInstalled", {"extension_id": extension_id})

    def discovered(self, extension_id: str) -> None:
        self._publish("ExtensionDiscovered", {"extension_id": extension_id})

    def validated(self, extension_id: str) -> None:
        self._publish("ExtensionValidated", {"extension_id": extension_id})

    def loaded(self, extension_id: str) -> None:
        self._publish("ExtensionLoaded", {"extension_id": extension_id})

    def initialized(self, extension_id: str) -> None:
        self._publish("ExtensionInitialized", {"extension_id": extension_id})

    def shutdown(self, extension_id: str) -> None:
        self._publish("ExtensionShutdown", {"extension_id": extension_id})

    def removed(self, extension_id: str) -> None:
        self._publish("ExtensionRemoved", {"extension_id": extension_id})

    def failed(self, extension_id: str, error: str) -> None:
        self._publish("ExtensionFailed", {"extension_id": extension_id, "error": error})

    def _publish(self, event_type: str, payload: dict[str, str]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=f"ext.{event_type}", payload=payload, source="extensions.runtime"))
