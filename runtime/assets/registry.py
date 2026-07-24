from __future__ import annotations

from runtime.assets.exceptions import AssetRegistrationFrozenError
from runtime.assets.lifecycle import AssetLifecycleState
from runtime.assets.metadata import AssetMetadata


class AssetEntry:
    def __init__(self, metadata: AssetMetadata, lifecycle: AssetLifecycleState = AssetLifecycleState.REGISTERED) -> None:
        self.metadata = metadata
        self.lifecycle = lifecycle
        self.dependencies: tuple[str, ...] = ()
        self.content: object = None
        self.content_type: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "metadata": self.metadata.to_dict(),
            "lifecycle": self.lifecycle.value,
            "dependencies": list(self.dependencies),
        }


class AssetRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, AssetEntry] = {}
        self._frozen = False

    def register(self, entry: AssetEntry) -> None:
        if self._frozen:
            from runtime.assets.exceptions import AssetRegistrationFrozenError
            raise AssetRegistrationFrozenError()
        if entry.metadata.asset_id in self._entries:
            from runtime.assets.exceptions import AssetConflictError
            raise AssetConflictError(entry.metadata.asset_id)
        self._entries[entry.metadata.asset_id] = entry

    def get(self, asset_id: str) -> AssetEntry | None:
        return self._entries.get(asset_id)

    def get_by_type(self, asset_type: str) -> tuple[AssetEntry, ...]:
        return tuple(e for e in self._entries.values() if e.metadata.asset_type == asset_type)

    def get_by_version(self, asset_type: str, version: str) -> tuple[AssetEntry, ...]:
        return tuple(e for e in self._entries.values() if e.metadata.asset_type == asset_type and e.metadata.version == version)

    def remove(self, asset_id: str) -> bool:
        if self._frozen:
            raise AssetRegistrationFrozenError()
        return self._entries.pop(asset_id, None) is not None

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def entries(self) -> dict[str, AssetEntry]:
        return dict(self._entries)

    @property
    def count(self) -> int:
        return len(self._entries)

    def __contains__(self, asset_id: str) -> bool:
        return asset_id in self._entries

    def __len__(self) -> int:
        return len(self._entries)
