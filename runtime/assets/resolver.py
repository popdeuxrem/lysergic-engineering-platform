from __future__ import annotations

from runtime.assets.registry import AssetEntry, AssetRegistry


class AssetResolver:
    def __init__(self, registry: AssetRegistry) -> None:
        self._registry = registry

    def resolve_urn(self, urn: str) -> AssetEntry | None:
        if not urn.startswith("urn:lep:asset:"):
            return None
        parts = urn.split(":")
        if len(parts) < 4:
            return None
        asset_id = parts[3]
        return self._registry.get(asset_id)

    def resolve(self, asset_id: str) -> AssetEntry | None:
        return self._registry.get(asset_id)

    def resolve_by_type_version(self, asset_type: str, version: str) -> tuple[AssetEntry, ...]:
        return self._registry.get_by_version(asset_type, version)
