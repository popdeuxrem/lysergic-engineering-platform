from __future__ import annotations

from copy import deepcopy
from typing import Any


def deep_merge(base: dict[str, Any], override: dict[str, Any], strategy: str = "override") -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value, strategy)
        elif key in result and strategy == "error":
            from runtime.configuration.exceptions import MergeConflictError
            raise MergeConflictError(key, result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def deep_merge_all(configs: list[dict[str, Any]], strategy: str = "override") -> dict[str, Any]:
    result: dict[str, Any] = {}
    for config in configs:
        result = deep_merge(result, config, strategy)
    return result


def filter_keys(data: dict[str, Any], prefix: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in data.items():
        if key.startswith(prefix):
            result[key] = deepcopy(value)
    return result


def flatten(data: dict[str, Any], parent_key: str = "", sep: str = ".") -> dict[str, Any]:
    items: list[tuple[str, Any]] = []
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def unflatten(data: dict[str, Any], sep: str = ".") -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in data.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = deepcopy(value)
    return result
