from __future__ import annotations

from runtime.services.events import Event, EventBus


class AssetEventPublisher:
    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus

    def registered(self, asset_id: str, asset_type: str, version: str) -> None:
        self._publish("AssetRegistered", {"asset_id": asset_id, "asset_type": asset_type, "version": version})

    def validated(self, asset_id: str) -> None:
        self._publish("AssetValidated", {"asset_id": asset_id})

    def available(self, asset_id: str) -> None:
        self._publish("AssetAvailable", {"asset_id": asset_id})

    def deprecated(self, asset_id: str) -> None:
        self._publish("AssetDeprecated", {"asset_id": asset_id})

    def removed(self, asset_id: str) -> None:
        self._publish("AssetRemoved", {"asset_id": asset_id})

    def failed(self, asset_id: str, error: str) -> None:
        self._publish("AssetFailed", {"asset_id": asset_id, "error": error})

    def _publish(self, event_type: str, payload: dict[str, str]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=f"asset.{event_type}", payload=payload, source="assets"))
