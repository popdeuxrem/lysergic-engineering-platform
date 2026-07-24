from __future__ import annotations

from extensions.sdk.manifest import ExtensionManifest
from runtime.api import LEP, RuntimeStatus
from runtime.extensions.discovery import FilesystemDiscovery
from runtime.extensions.lifecycle import (
    ExtensionRuntimeLifecycle,
    RuntimeLifecycleState,
)
from runtime.extensions.manifest import ExtensionManifestLoader
from runtime.extensions.registry import ExtensionRuntimeRecord, ExtensionRuntimeRegistry
from runtime.extensions.snapshot import ExtensionRuntimeSnapshot
from runtime.extensions.validator import ExtensionRuntimeValidator


class ExtensionRuntimeManager:
    service_id = "extensions.runtime"
    dependencies: tuple[str, ...] = ()

    def __init__(self, lep: LEP | None = None) -> None:
        self._registry = ExtensionRuntimeRegistry()
        self._lifecycle = ExtensionRuntimeLifecycle()
        self._loader = ExtensionManifestLoader()
        self._discovery = FilesystemDiscovery()
        self._validator = ExtensionRuntimeValidator()
        self._lep = lep
        self._snapshot_version = 0
        self._snapshot: ExtensionRuntimeSnapshot | None = None
        self._initialized = False

    @property
    def registry(self) -> ExtensionRuntimeRegistry:
        return self._registry

    @property
    def lifecycle(self) -> ExtensionRuntimeLifecycle:
        return self._lifecycle

    @property
    def snapshot(self) -> ExtensionRuntimeSnapshot | None:
        return self._snapshot

    @property
    def manager_status(self) -> RuntimeStatus:
        return RuntimeStatus.READY if self._initialized else RuntimeStatus.PENDING

    def initialize(self) -> None:
        if self._initialized:
            return
        self._snapshot_version = 0
        self._initialized = True
        self._freeze_snapshot()

    def shutdown(self) -> None:
        self._registry = ExtensionRuntimeRegistry()
        self._snapshot = None
        self._initialized = False

    def install(self, path: str) -> ExtensionRuntimeRecord:
        manifest = self._loader.load(path)
        self._validator.validate_manifest(manifest)
        record = ExtensionRuntimeRecord(extension_id=manifest.extension_id, manifest=manifest, state="installed", install_path=path)
        self._registry.register(record)
        self._lifecycle.install(manifest.extension_id)
        self._freeze_snapshot()
        return record

    def discover(self, extension_id: str) -> ExtensionRuntimeRecord | None:
        record = self._registry.get(extension_id)
        if record is None:
            return None
        self._lifecycle.transition(extension_id, RuntimeLifecycleState.DISCOVERED)
        self._registry.set_state(extension_id, "discovered")
        self._freeze_snapshot()
        return record

    def validate_extension(self, extension_id: str) -> ExtensionRuntimeRecord | None:
        record = self._registry.get(extension_id)
        if record is None:
            return None
        try:
            available = {r.extension_id for r in self._registry.list()}
            self._validator.validate_manifest(record.manifest)
            self._validator.validate_dependencies(record.manifest, available)
            self._lifecycle.transition(extension_id, RuntimeLifecycleState.VALIDATED)
            self._registry.set_state(extension_id, "validated")
        except Exception as e:  # noqa: BLE001
            self._lifecycle.transition(extension_id, RuntimeLifecycleState.FAILED)
            self._registry.set_state(extension_id, "failed")
            self._registry.set_error(extension_id, str(e))
        self._freeze_snapshot()
        return record

    def load(self, extension_id: str) -> ExtensionRuntimeRecord | None:
        record = self._registry.get(extension_id)
        if record is None:
            return None
        self._lifecycle.transition(extension_id, RuntimeLifecycleState.LOADED)
        self._registry.set_state(extension_id, "loaded")
        self._freeze_snapshot()
        return record

    def initialize_extension(self, extension_id: str) -> ExtensionRuntimeRecord | None:
        record = self._registry.get(extension_id)
        if record is None:
            return None
        self._lifecycle.transition(extension_id, RuntimeLifecycleState.INITIALIZED)
        self._registry.set_state(extension_id, "initialized")
        self._freeze_snapshot()
        return record

    def shutdown_extension(self, extension_id: str) -> ExtensionRuntimeRecord | None:
        record = self._registry.get(extension_id)
        if record is None:
            return None
        self._lifecycle.transition(extension_id, RuntimeLifecycleState.SHUTDOWN)
        self._registry.set_state(extension_id, "shutdown")
        self._freeze_snapshot()
        return record

    def remove(self, extension_id: str) -> bool:
        if extension_id not in self._registry:
            return False
        self._lifecycle.transition(extension_id, RuntimeLifecycleState.REMOVED)
        self._registry.unregister(extension_id)
        self._freeze_snapshot()
        return True

    def get(self, extension_id: str) -> ExtensionRuntimeRecord | None:
        return self._registry.get(extension_id)

    def list(self) -> tuple[ExtensionRuntimeRecord, ...]:
        return self._registry.list()

    def status(self, extension_id: str) -> str | None:
        state = self._lifecycle.state_of(extension_id)
        return state.value if state else None

    def discover_all(self) -> tuple[ExtensionManifest, ...]:
        return self._discovery.discover()

    def snapshot_state(self) -> ExtensionRuntimeSnapshot:
        records = {r.extension_id: r for r in self._registry.list()}
        return ExtensionRuntimeSnapshot(records=records, version=self._snapshot_version)

    def _freeze_snapshot(self) -> None:
        self._snapshot_version += 1
        records = {r.extension_id: r for r in self._registry.list()}
        self._snapshot = ExtensionRuntimeSnapshot(records=records, version=self._snapshot_version)
