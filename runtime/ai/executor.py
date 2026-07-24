from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ModelProvider(Protocol):
    provider_id: str

    def execute(self, prompt: str, context: dict[str, Any] | None = None) -> str: ...

    @property
    def model_name(self) -> str: ...


class InProcessProvider:
    provider_id = "inprocess"

    def __init__(self, model_name: str = "mock") -> None:
        self._model_name = model_name

    def execute(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        return f"mock[{self._model_name}]: {prompt[:50]}..."

    @property
    def model_name(self) -> str:
        return self._model_name


class AIExecutor:
    def __init__(self) -> None:
        self._providers: dict[str, ModelProvider] = {}
        self._default = InProcessProvider()

    def register_provider(self, provider: ModelProvider) -> None:
        self._providers[provider.provider_id] = provider

    def execute(self, prompt: str, context: dict[str, Any] | None = None, provider_id: str = "") -> str:
        provider = self._providers.get(provider_id, self._default)
        return provider.execute(prompt, context)

    @property
    def default_provider(self) -> ModelProvider:
        return self._default
