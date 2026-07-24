from __future__ import annotations

from typing import Any

from runtime.assets.cache import AssetCache
from runtime.assets.catalog import AssetCatalog
from runtime.assets.dependency import AssetDependencyGraph
from runtime.assets.events import AssetEventPublisher
from runtime.assets.exceptions import InvalidLifecycleTransitionError
from runtime.assets.lifecycle import AssetLifecycle, AssetLifecycleState
from runtime.assets.loader import AssetLoader, RepositoryProvider
from runtime.assets.metadata import AssetMetadata
from runtime.assets.registry import AssetEntry, AssetRegistry
from runtime.assets.resolver import AssetResolver
from runtime.assets.search import AssetSearch
from runtime.assets.snapshot import AssetSnapshot
from runtime.assets.validation import AssetValidator
from runtime.services.events import EventBus
from runtime.services.registry import ServiceStatus


class AssetManager:
    service_id = "asset.manager"
    dependencies: tuple[str, ...] = ()

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._registry = AssetRegistry()
        self._lifecycle = AssetLifecycle()
        self._catalog = AssetCatalog()
        self._dependency = AssetDependencyGraph()
        self._cache = AssetCache()
        self._search = AssetSearch(self._catalog)
        self._resolver = AssetResolver(self._registry)
        self._validator = AssetValidator()
        self._validator = AssetValidator()
        self._loader = AssetLoader()
        self._events = AssetEventPublisher(event_bus)
        self._snapshot_version = 0
        self._snapshot: AssetSnapshot | None = None
        self._initialized = False
        self._loader.add_provider(RepositoryProvider())

    @property
    def registry(self) -> AssetRegistry:
        return self._registry

    @property
    def lifecycle(self) -> AssetLifecycle:
        return self._lifecycle

    @property
    def catalog(self) -> AssetCatalog:
        return self._catalog

    @property
    def dependency(self) -> AssetDependencyGraph:
        return self._dependency

    @property
    def cache(self) -> AssetCache:
        return self._cache

    @property
    def search(self) -> AssetSearch:
        return self._search

    @property
    def resolver(self) -> AssetResolver:
        return self._resolver

    @property
    def validator(self) -> AssetValidator:
        return self._validator

    @property
    def loader(self) -> AssetLoader:
        return self._loader

    @property
    def snapshot(self) -> AssetSnapshot | None:
        return self._snapshot

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY if self._initialized else ServiceStatus.PENDING

    def initialize(self) -> None:
        if self._initialized:
            return
        self._registry = AssetRegistry()
        self._lifecycle = AssetLifecycle()
        self._catalog = AssetCatalog()
        self._search = AssetSearch(self._catalog)
        self._resolver = AssetResolver(self._registry)
        self._dependency = AssetDependencyGraph()
        self._cache = AssetCache()
        self._snapshot_version = 0
        self._initialized = True
        self._freeze_snapshot()

    def shutdown(self) -> None:
        self._cache.clear()
        self._registry = AssetRegistry()
        self._snapshot = None
        self._initialized = False

    def register(self, metadata: AssetMetadata, dependencies: tuple[str, ...] = ()) -> AssetEntry:
        entry = AssetEntry(metadata=metadata)
        entry.dependencies = dependencies
        self._registry.register(entry)
        self._lifecycle.initialize(metadata.asset_id)
        self._catalog.index(metadata)
        self._dependency.register(metadata.asset_id, dependencies)
        self._events.registered(metadata.asset_id, metadata.asset_type, metadata.version)
        self._freeze_snapshot()
        return entry

    def get(self, asset_id: str) -> AssetEntry | None:
        cached: AssetEntry | None = self._cache.get(asset_id)
        if cached is not None:
            return cached
        entry = self._registry.get(asset_id)
        if entry is not None:
            self._cache.set(asset_id, entry)
        return entry

    def list(self, asset_type: str | None = None) -> tuple[AssetEntry, ...]:
        if asset_type is None:
            return tuple(self._registry.entries.values())
        return self._registry.get_by_type(asset_type)

    def validate(self, asset_id: str) -> AssetEntry | None:
        entry = self._registry.get(asset_id)
        if entry is None:
            return None
        vr = self._validator.validate(entry.metadata)
        if vr.valid:
            try:
                self._lifecycle.transition(asset_id, AssetLifecycleState.VALIDATED)
            except InvalidLifecycleTransitionError:
                pass
            self._events.validated(asset_id)
            self._cache.invalidate(asset_id)
        else:
            self._events.failed(asset_id, "; ".join(vr.tier1_errors))
        self._freeze_snapshot()
        return entry

    def activate(self, asset_id: str) -> AssetEntry | None:
        entry = self._registry.get(asset_id)
        if entry is None:
            return None
        try:
            self._lifecycle.transition(asset_id, AssetLifecycleState.AVAILABLE)
            self._events.available(asset_id)
            self._cache.invalidate(asset_id)
        except InvalidLifecycleTransitionError:
            pass
        self._freeze_snapshot()
        return entry

    def deprecate(self, asset_id: str) -> AssetEntry | None:
        entry = self._registry.get(asset_id)
        if entry is None:
            return None
        try:
            self._lifecycle.transition(asset_id, AssetLifecycleState.DEPRECATED)
            self._events.deprecated(asset_id)
            self._cache.invalidate(asset_id)
        except InvalidLifecycleTransitionError:
            pass
        self._freeze_snapshot()
        return entry

    def remove(self, asset_id: str) -> bool:
        if asset_id not in self._registry:
            return False
        try:
            self._lifecycle.transition(asset_id, AssetLifecycleState.REMOVED)
        except InvalidLifecycleTransitionError:
            pass
        self._registry.remove(asset_id)
        self._catalog.remove(asset_id)
        self._dependency.remove(asset_id)
        self._cache.invalidate(asset_id)
        self._events.removed(asset_id)
        self._freeze_snapshot()
        return True

    def search_assets(self, query: str, asset_type: str | None = None) -> tuple[dict[str, Any], ...]:
        return self._search.search(query, asset_type)

    def resolve(self, asset_id: str) -> AssetEntry | None:
        return self._resolver.resolve(asset_id)

    def resolve_urn(self, urn: str) -> AssetEntry | None:
        return self._resolver.resolve_urn(urn)

    def snapshot_state(self) -> AssetSnapshot:
        return AssetSnapshot(entries=self._registry.entries, version=self._snapshot_version)

    def _freeze_snapshot(self) -> None:
        self._snapshot_version += 1
        self._snapshot = AssetSnapshot(entries=self._registry.entries, version=self._snapshot_version)
