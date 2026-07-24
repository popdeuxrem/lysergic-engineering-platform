from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol, runtime_checkable


class ConfigSource(Enum):
    DEFAULT = 0
    PROFILE = 10
    ENVIRONMENT = 20
    PROVIDER = 30
    RUNTIME_OVERRIDE = 40


@runtime_checkable
class ConfigurationProvider(Protocol):
    provider_id: str
    source: ConfigSource

    def load(self) -> dict[str, Any]: ...

    @property
    def priority(self) -> int: ...


@dataclass
class ProviderRegistration:
    provider_id: str
    provider: ConfigurationProvider
    source: ConfigSource = ConfigSource.PROVIDER
    priority: int = 0
    enabled: bool = True


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderRegistration] = {}
        self._frozen = False

    def register(self, registration: ProviderRegistration) -> None:
        if self._frozen:
            raise RuntimeError("Provider registry is frozen")
        if registration.provider_id in self._providers:
            raise ValueError(f"Provider '{registration.provider_id}' already registered")
        self._providers[registration.provider_id] = registration

    def unregister(self, provider_id: str) -> bool:
        if self._frozen:
            raise RuntimeError("Provider registry is frozen")
        return self._providers.pop(provider_id, None) is not None

    def get(self, provider_id: str) -> ProviderRegistration:
        if provider_id not in self._providers:
            from runtime.configuration.exceptions import ProviderNotFoundError
            raise ProviderNotFoundError(provider_id)
        return self._providers[provider_id]

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def providers(self) -> dict[str, ProviderRegistration]:
        return dict(self._providers)

    @property
    def count(self) -> int:
        return len(self._providers)

    def __contains__(self, provider_id: str) -> bool:
        return provider_id in self._providers
