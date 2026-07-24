from __future__ import annotations

from typing import Any

from runtime.configuration.provider import ConfigSource


class LayerResolver:
    def __init__(self) -> None:
        self._layers: dict[ConfigSource, dict[str, Any]] = {s: {} for s in ConfigSource}

    def set_layer(self, source: ConfigSource, data: dict[str, Any]) -> None:
        self._layers[source] = dict(data)

    def get_layer(self, source: ConfigSource) -> dict[str, Any]:
        return dict(self._layers.get(source, {}))

    def resolve(self, key: str) -> tuple[Any, ConfigSource | None]:
        for source in sorted(ConfigSource, key=lambda s: s.value, reverse=True):
            if key in self._layers.get(source, {}):
                return self._layers[source][key], source
        return None, None

    def resolve_all(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for source in sorted(ConfigSource, key=lambda s: s.value):
            from runtime.configuration.merge import deep_merge
            result = deep_merge(result, self._layers.get(source, {}))
        return result

    def resolve_with_source(self) -> dict[str, tuple[Any, ConfigSource]]:
        result: dict[str, tuple[Any, ConfigSource]] = {}
        seen: set[str] = set()
        for source in sorted(ConfigSource, key=lambda s: s.value, reverse=True):
            for key, value in self._layers.get(source, {}).items():
                if key not in seen:
                    result[key] = (value, source)
                    seen.add(key)
        return result

    @property
    def layer_count(self) -> int:
        return sum(1 for layer in self._layers.values() if layer)

    def clear(self) -> None:
        for s in ConfigSource:
            self._layers[s] = {}
