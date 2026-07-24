from __future__ import annotations

from typing import Any

from runtime.configuration.loader import EnvProvider, FileLoader
from runtime.configuration.merge import deep_merge
from runtime.configuration.profile import ProfileManager
from runtime.configuration.provider import ConfigSource, ProviderRegistry
from runtime.configuration.resolver import LayerResolver
from runtime.configuration.snapshot import ConfigSnapshot
from runtime.configuration.validation import ConfigValidator
from runtime.configuration.watcher import ConfigWatcher
from runtime.services.events import Event, EventBus
from runtime.services.health import HealthService
from runtime.services.registry import ServiceStatus


class ConfigurationManager:
    service_id = "config.manager"
    dependencies: tuple[str, ...] = ()

    def __init__(
        self,
        event_bus: EventBus | None = None,
        health: HealthService | None = None,
    ) -> None:
        self._event_bus = event_bus
        self._health = health
        self._loader = FileLoader()
        self._provider_registry = ProviderRegistry()
        self._profile_manager = ProfileManager()
        self._layer_resolver = LayerResolver()
        self._validator = ConfigValidator()
        self._watcher = ConfigWatcher()
        self._snapshot: ConfigSnapshot | None = None
        self._version = 0
        self._initialized = False

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY if self._initialized else ServiceStatus.PENDING

    @property
    def provider_registry(self) -> ProviderRegistry:
        return self._provider_registry

    @property
    def profile_manager(self) -> ProfileManager:
        return self._profile_manager

    @property
    def validator(self) -> ConfigValidator:
        return self._validator

    @property
    def watcher(self) -> ConfigWatcher:
        return self._watcher

    @property
    def snapshot(self) -> ConfigSnapshot | None:
        return self._snapshot

    def initialize(self) -> None:
        if self._initialized:
            return
        self._load_defaults()
        self._load_environment()
        self._load_providers()
        self._resolve()
        self._validate()
        self._snapshot = self._create_snapshot("initialized")
        self._provider_registry.freeze()
        self._initialized = True
        self._publish("config.initialized", {"version": self._version})

    def shutdown(self) -> None:
        self._watcher.disable()
        self._layer_resolver.clear()
        self._snapshot = None
        self._initialized = False
        self._publish("config.stopped", {})

    def load_file(self, path: str) -> None:
        data = self._loader.load_yaml(path)
        self._layer_resolver.set_layer(ConfigSource.PROFILE, data)
        self._reload()

    def set_override(self, key: str, value: Any) -> None:
        overrides = self._layer_resolver.get_layer(ConfigSource.RUNTIME_OVERRIDE)
        keys = key.split(".")
        current = overrides
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        self._layer_resolver.set_layer(ConfigSource.RUNTIME_OVERRIDE, overrides)
        self._reload()

    def get(self, key: str, default: Any = None) -> Any:
        if self._snapshot is not None:
            return self._snapshot.get(key, default)
        value, _ = self._layer_resolver.resolve(key)
        return value if value is not None else default

    def has(self, key: str) -> bool:
        if self._snapshot is not None:
            return self._snapshot.has(key)
        value, _ = self._layer_resolver.resolve(key)
        return value is not None

    def all(self) -> dict[str, Any]:
        if self._snapshot is not None:
            return dict(self._snapshot.config)
        return self._layer_resolver.resolve_all()

    def resolve_with_source(self) -> dict[str, tuple[Any, ConfigSource]]:
        return self._layer_resolver.resolve_with_source()

    def _load_defaults(self) -> None:
        defaults = {
            "platform": {"name": "Lysergic Engineering Platform", "version": "0.1.0", "architecture": "LEP-ARCH-v0.1.0"},
            "validation": {"schema": {"dialect": "draft2020-12"}},
            "governance": {"enabled": True},
            "runtime": {"execution_model": {"enabled": True}},
        }
        self._layer_resolver.set_layer(ConfigSource.DEFAULT, defaults)

    def _load_environment(self) -> None:
        env_provider = EnvProvider()
        data = env_provider.load()
        if data:
            self._layer_resolver.set_layer(ConfigSource.ENVIRONMENT, data)

    def _load_providers(self) -> None:
        merged: dict[str, Any] = {}
        for reg in self._provider_registry.providers.values():
            if reg.enabled:
                try:
                    data = reg.provider.load()
                    merged = deep_merge(merged, data)
                except Exception:  # noqa: BLE001, S110
                    pass
        if merged:
            self._layer_resolver.set_layer(ConfigSource.PROVIDER, merged)

    def _resolve(self) -> None:
        profile_config = {}
        if self._profile_manager.active:
            profile_config = self._profile_manager.resolved_config()
        if profile_config:
            self._layer_resolver.set_layer(ConfigSource.PROFILE, profile_config)
        self._version += 1

    def _validate(self) -> None:
        resolved = self._layer_resolver.resolve_all()
        result = self._validator.validate(resolved)
        if not result.valid:
            self._publish("config.validation_failed", {"errors": list(result.errors)})

    def _create_snapshot(self, source: str) -> ConfigSnapshot:
        return ConfigSnapshot(
            config=self._layer_resolver.resolve_all(),
            source=source,
            version=self._version,
            profile=self._profile_manager.active,
        )

    def _reload(self) -> None:
        old = self._snapshot
        self._resolve()
        self._validate()
        self._snapshot = self._create_snapshot("reload")
        if old is not None:
            self._detect_changes(old.config, self._snapshot.config)
        self._publish("config.reloaded", {"version": self._version})

    def _detect_changes(self, old: dict[str, Any], new: dict[str, Any]) -> None:
        all_keys = set(old) | set(new)
        for key in all_keys:
            old_val = old.get(key)
            new_val = new.get(key)
            if old_val != new_val:
                self._watcher.notify(key, old_val, new_val)

    def _publish(self, event_type: str, payload: dict[str, Any]) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(Event(event_type=event_type, payload=payload, source="configuration"))
