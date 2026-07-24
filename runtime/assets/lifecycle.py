from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any


class AssetLifecycleState(Enum):
    REGISTERED = "registered"
    VALIDATED = "validated"
    AVAILABLE = "available"
    DEPRECATED = "deprecated"
    REMOVED = "removed"


_ASSET_TRANSITIONS: dict[AssetLifecycleState, tuple[AssetLifecycleState, ...]] = {
    AssetLifecycleState.REGISTERED: (AssetLifecycleState.VALIDATED, AssetLifecycleState.REMOVED),
    AssetLifecycleState.VALIDATED: (AssetLifecycleState.AVAILABLE, AssetLifecycleState.DEPRECATED, AssetLifecycleState.REMOVED),
    AssetLifecycleState.AVAILABLE: (AssetLifecycleState.DEPRECATED, AssetLifecycleState.VALIDATED, AssetLifecycleState.REMOVED),
    AssetLifecycleState.DEPRECATED: (AssetLifecycleState.REMOVED, AssetLifecycleState.AVAILABLE),
    AssetLifecycleState.REMOVED: (),
}


class AssetLifecycle:
    def __init__(self) -> None:
        self._states: dict[str, AssetLifecycleState] = {}
        self._transitions: list[dict[str, Any]] = []

    def initialize(self, asset_id: str) -> None:
        self._states[asset_id] = AssetLifecycleState.REGISTERED
        self._record(asset_id, AssetLifecycleState.REGISTERED)

    def transition(self, asset_id: str, target: AssetLifecycleState) -> AssetLifecycleState:
        current = self._states.get(asset_id)
        if current is None:
            raise KeyError(f"Asset not found: {asset_id}")
        allowed = _ASSET_TRANSITIONS.get(current, ())
        if target not in allowed:
            from runtime.assets.exceptions import InvalidLifecycleTransitionError
            raise InvalidLifecycleTransitionError(current.value, target.value)
        self._states[asset_id] = target
        self._record(asset_id, target)
        return target

    def state_of(self, asset_id: str) -> AssetLifecycleState | None:
        return self._states.get(asset_id)

    @property
    def history(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._transitions)

    def _record(self, asset_id: str, state: AssetLifecycleState) -> None:
        self._transitions.append({
            "asset_id": asset_id, "state": state.value, "timestamp": datetime.now(UTC).isoformat(),
        })
