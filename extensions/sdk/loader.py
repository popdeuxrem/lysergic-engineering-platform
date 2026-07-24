from __future__ import annotations

from typing import Any

from extensions.sdk.capabilities import CapabilityRegistration, CapabilityRegistry
from extensions.sdk.compatibility import CompatibilityChecker
from extensions.sdk.dependencies import DependencyResolver
from extensions.sdk.extension import Extension
from extensions.sdk.lifecycle import ExtensionLifecycle, ExtensionLifecycleState
from extensions.sdk.manifest import ExtensionManifest, ManifestValidationError
from extensions.sdk.registry import ExtensionRegistry, ExtensionState
from extensions.sdk.validation import ValidationEngine
from runtime.services.events import Event, EventBus
from runtime.services.manager import ServiceManager


class ExtensionLoader:
    def __init__(
        self,
        registry: ExtensionRegistry,
        lifecycle: ExtensionLifecycle,
        capability_registry: CapabilityRegistry,
        resolver: DependencyResolver,
        validator: ValidationEngine,
        compatibility: CompatibilityChecker,
        event_bus: EventBus | None = None,
        manager: ServiceManager | None = None,
    ) -> None:
        self._registry = registry
        self._lifecycle = lifecycle
        self._capabilities = capability_registry
        self._resolver = resolver
        self._validator = validator
        self._compatibility = compatibility
        self._event_bus = event_bus
        self._manager = manager

    def discover(self, manifest: ExtensionManifest) -> ExtensionState:
        self._lifecycle.register(manifest.extension_id)
        self._registry.store(manifest)
        self._lifecycle.transition(manifest.extension_id, ExtensionLifecycleState.VALIDATED)
        self._publish("ExtensionDiscovered", {"extension_id": manifest.extension_id, "name": manifest.name, "version": manifest.version})
        state = self._registry.get(manifest.extension_id)
        assert state is not None
        return state

    def validate(self, extension_id: str) -> ExtensionState | None:
        manifest = self._registry.manifest(extension_id)
        if manifest is None:
            return None
        try:
            self._validator.validate_manifest(manifest)
        except ManifestValidationError as exc:
            self._lifecycle.transition(extension_id, ExtensionLifecycleState.FAILED, str(exc))
            self._publish("ExtensionFailed", {"extension_id": extension_id, "error": str(exc)})
            return self._registry.get(extension_id)
        current = self._lifecycle.state_of(extension_id)
        if current == ExtensionLifecycleState.VALIDATED:
            self._lifecycle.transition(extension_id, ExtensionLifecycleState.LOADING)
        self._publish("ExtensionValidated", {"extension_id": extension_id})
        return self._registry.get(extension_id)

    def load(self, extension_id: str, extension: Extension | None = None) -> ExtensionState | None:
        manifest = self._registry.manifest(extension_id)
        if manifest is None:
            return None
        deps_resolved = self._resolver.resolve()
        for dep_id in self._resolver.dependencies_of(extension_id):
            if dep_id not in deps_resolved and not self._resolver.is_optional(dep_id):
                self._lifecycle.transition(extension_id, ExtensionLifecycleState.FAILED, f"Unresolved dependency: {dep_id}")
                self._publish("ExtensionFailed", {"extension_id": extension_id, "error": f"Unresolved dependency: {dep_id}"})
                return self._registry.get(extension_id)
        self._registry.set_state(extension_id, ExtensionState.LOADING)
        self._publish("ExtensionLoaded", {"extension_id": extension_id})
        if extension is not None:
            extension.initialize()
            self._registry.set_extension(extension_id, extension)
        for cap_id in manifest.capabilities:
            self._capabilities.register(CapabilityRegistration(
                capability_id=cap_id,
                provider_id=extension_id,
                version=manifest.version,
            ))
        self._lifecycle.transition(extension_id, ExtensionLifecycleState.READY)
        self._registry.set_state(extension_id, ExtensionState.READY)
        self._publish("ExtensionReady", {"extension_id": extension_id})
        return self._registry.get(extension_id)

    def unload(self, extension_id: str) -> ExtensionState | None:
        manifest = self._registry.manifest(extension_id)
        if manifest is None:
            return None
        for cap_id in manifest.capabilities:
            self._capabilities.remove_provider(cap_id, extension_id)
        extension = self._registry.get_extension(extension_id)
        if extension is not None:
            try:
                extension.shutdown()
            except Exception:  # noqa: BLE001, S110
                pass
        self._lifecycle.transition(extension_id, ExtensionLifecycleState.STOPPED)
        self._registry.set_state(extension_id, ExtensionState.STOPPED)
        self._publish("ExtensionStopped", {"extension_id": extension_id})
        return self._registry.get(extension_id)

    def remove(self, extension_id: str) -> bool:
        state = self._registry.get(extension_id)
        if state is None:
            return False
        self._lifecycle.transition(extension_id, ExtensionLifecycleState.REMOVED)
        self._registry.remove(extension_id)
        self._publish("ExtensionRemoved", {"extension_id": extension_id})
        return True

    def _publish(self, event_type: str, payload: dict[str, Any]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=f"extension.{event_type}", payload=payload, source="extensions.sdk"))
