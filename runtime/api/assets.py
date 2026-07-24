from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


@dataclass
class AssetRecord:
    asset_id: str
    asset_type: str
    version: str = "0.1.0"
    description: str = ""
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


ASSET_TYPES = ("schema", "template", "contract", "profile", "documentation")


class AssetsAPIProtocol(Protocol):
    def store(self, asset_id: str, asset_type: str, **kwargs: Any) -> AssetRecord: ...
    def get(self, asset_id: str) -> AssetRecord | None: ...
    def list(self, asset_type: str | None = None) -> tuple[AssetRecord, ...]: ...
    def list_by_type(self, asset_type: str) -> tuple[AssetRecord, ...]: ...
    def list_types(self) -> tuple[str, ...]: ...
    def search(self, query: str) -> tuple[AssetRecord, ...]: ...
    def remove(self, asset_id: str) -> bool: ...
    def count(self, asset_type: str | None = None) -> int: ...
    def tag(self, asset_id: str, tags: tuple[str, ...]) -> bool: ...


class AssetsAPI:
    service_id = "api.assets"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._assets: dict[str, AssetRecord] = {}

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._assets.clear()

    def store(self, asset_id: str, asset_type: str, **kwargs: Any) -> AssetRecord:
        record = AssetRecord(asset_id=asset_id, asset_type=asset_type, **kwargs)
        self._assets[asset_id] = record
        return record

    def get(self, asset_id: str) -> AssetRecord | None:
        return self._assets.get(asset_id)

    def list(self, asset_type: str | None = None) -> tuple[AssetRecord, ...]:
        if asset_type is None:
            return tuple(self._assets.values())
        return tuple(a for a in self._assets.values() if a.asset_type == asset_type)

    def list_by_type(self, asset_type: str) -> tuple[AssetRecord, ...]:
        return tuple(a for a in self._assets.values() if a.asset_type == asset_type)

    def list_types(self) -> tuple[str, ...]:
        return tuple(sorted({a.asset_type for a in self._assets.values()}))

    def search(self, query: str) -> tuple[AssetRecord, ...]:
        q = query.lower()
        return tuple(
            a for a in self._assets.values()
            if q in a.asset_id.lower() or q in a.description.lower() or any(q in t.lower() for t in a.tags)
        )

    def remove(self, asset_id: str) -> bool:
        if asset_id in self._assets:
            del self._assets[asset_id]
            return True
        return False

    def count(self, asset_type: str | None = None) -> int:
        if asset_type is None:
            return len(self._assets)
        return sum(1 for a in self._assets.values() if a.asset_type == asset_type)

    def tag(self, asset_id: str, tags: tuple[str, ...]) -> bool:
        if asset_id not in self._assets:
            return False
        record = self._assets[asset_id]
        existing = set(record.tags)
        existing.update(tags)
        self._assets[asset_id] = AssetRecord(
            asset_id=record.asset_id, asset_type=record.asset_type,
            version=record.version, description=record.description,
            tags=tuple(sorted(existing)), created_at=record.created_at, metadata=record.metadata,
        )
        return True


def create_assets_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(service_id="api.assets", factory=lambda: AssetsAPI(manager))
