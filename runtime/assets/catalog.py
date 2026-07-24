from __future__ import annotations

from typing import Any

from runtime.assets.metadata import AssetMetadata


class AssetCatalog:
    def __init__(self) -> None:
        self._index: dict[str, dict[str, Any]] = {}

    def index(self, metadata: AssetMetadata) -> None:
        self._index[metadata.asset_id] = {
            "asset_id": metadata.asset_id,
            "asset_type": metadata.asset_type,
            "version": metadata.version,
            "owner": metadata.owner,
            "description": metadata.description,
            "tags": metadata.tags,
            "origin": metadata.origin,
        }

    def remove(self, asset_id: str) -> bool:
        return self._index.pop(asset_id, None) is not None

    def get(self, asset_id: str) -> dict[str, Any] | None:
        return self._index.get(asset_id)

    def filter(self, asset_type: str | None = None, owner: str | None = None, tag: str | None = None) -> tuple[dict[str, Any], ...]:
        results = list(self._index.values())
        if asset_type is not None:
            results = [r for r in results if r["asset_type"] == asset_type]
        if owner is not None:
            results = [r for r in results if r["owner"] == owner]
        if tag is not None:
            results = [r for r in results if tag in r["tags"]]
        return tuple(results)

    @property
    def entries(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._index.values())

    @property
    def count(self) -> int:
        return len(self._index)
