from __future__ import annotations

from pathlib import Path
from typing import Any


class AssetContent:
    def __init__(self, data: Any, content_type: str = "application/octet-stream") -> None:
        self.data = data
        self.content_type = content_type


class AssetLoaderProvider:
    def load(self, asset_id: str, source: str) -> AssetContent | None: ...


class RepositoryProvider(AssetLoaderProvider):
    def __init__(self, base_path: str | None = None) -> None:
        self._base_path = Path(base_path) if base_path else Path.cwd()

    def load(self, asset_id: str, source: str) -> AssetContent | None:
        path = self._base_path / source
        if not path.exists():
            return None
        try:
            data = path.read_bytes()
            return AssetContent(data=data, content_type="application/octet-stream")
        except Exception:  # noqa: BLE001
            return None

    def set_base_path(self, path: str) -> None:
        self._base_path = Path(path)


class AssetLoader:
    def __init__(self) -> None:
        self._providers: list[AssetLoaderProvider] = []

    def add_provider(self, provider: AssetLoaderProvider) -> None:
        self._providers.append(provider)

    def load(self, asset_id: str, source: str) -> AssetContent | None:
        for provider in self._providers:
            content = provider.load(asset_id, source)
            if content is not None:
                return content
        return None
