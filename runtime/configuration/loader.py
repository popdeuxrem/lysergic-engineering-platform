from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from runtime.configuration.provider import ConfigSource


class FileLoader:
    def __init__(self) -> None:
        self._loaded_files: set[str] = set()

    def load_yaml(self, path: str | Path) -> dict[str, Any]:
        resolved = Path(path).resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"Configuration file not found: {resolved}")
        with open(resolved) as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise TypeError(f"Configuration file must contain a mapping: {resolved}")
        self._loaded_files.add(str(resolved))
        return dict(data)

    def load_env(self, prefix: str = "LEP_") -> dict[str, Any]:
        import os
        result: dict[str, Any] = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower().replace("__", ".").replace("_", ".")
                result[config_key] = value
        return result

    @property
    def loaded_files(self) -> tuple[str, ...]:
        return tuple(self._loaded_files)


class EnvProvider:
    provider_id = "env"
    source = ConfigSource.ENVIRONMENT

    def __init__(self, prefix: str = "LEP_") -> None:
        self._prefix = prefix
        self._priority = ConfigSource.ENVIRONMENT.value

    def load(self) -> dict[str, Any]:
        loader = FileLoader()
        return loader.load_env(self._prefix)

    @property
    def priority(self) -> int:
        return self._priority


class YamlFileProvider:
    provider_id = "yaml"
    source = ConfigSource.PROFILE

    def __init__(self, path: str | Path, priority: int = 0) -> None:
        self._path = Path(path)
        self._priority = priority

    def load(self) -> dict[str, Any]:
        loader = FileLoader()
        return loader.load_yaml(self._path)

    @property
    def priority(self) -> int:
        return self._priority
