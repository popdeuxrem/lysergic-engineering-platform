from __future__ import annotations

from typing import Any

from runtime.assets.catalog import AssetCatalog


class AssetSearch:
    def __init__(self, catalog: AssetCatalog) -> None:
        self._catalog = catalog

    def search(self, query: str, asset_type: str | None = None) -> tuple[dict[str, Any], ...]:
        q = query.lower()
        results = list(self._catalog.entries)
        results = [r for r in results if q in r["asset_id"].lower() or q in r["description"].lower() or any(q in t.lower() for t in r["tags"])]
        if asset_type is not None:
            results = [r for r in results if r["asset_type"] == asset_type]
        return tuple(results)

    def search_by_tag(self, tag: str) -> tuple[dict[str, Any], ...]:
        return self._catalog.filter(tag=tag)

    def search_by_type(self, asset_type: str) -> tuple[dict[str, Any], ...]:
        return self._catalog.filter(asset_type=asset_type)

    def search_by_owner(self, owner: str) -> tuple[dict[str, Any], ...]:
        return self._catalog.filter(owner=owner)
