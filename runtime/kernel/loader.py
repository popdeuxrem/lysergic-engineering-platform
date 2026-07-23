from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class KernelConfig:
    platform_name: str
    platform_identifier: str
    platform_version: str
    architecture_baseline_id: str
    architecture_status: str
    metamodel_ecp_version: str
    metamodel_ecp_status: str
    schema_dialect: str
    governance_enabled: bool
    runtime_enabled: bool

    @classmethod
    def from_manifest(cls, manifest: dict[str, Any]) -> KernelConfig:
        platform = manifest["platform"]
        arch = manifest["architecture"]
        meta = manifest["metamodel"]
        runtime = manifest["runtime"]
        validation = manifest["validation"]
        gov = manifest["governance"]

        return cls(
            platform_name=platform["name"],
            platform_identifier=platform["identifier"],
            platform_version=platform["version"],
            architecture_baseline_id=arch["baseline"]["id"],
            architecture_status=arch["baseline"]["status"],
            metamodel_ecp_version=meta["ecp"]["version"],
            metamodel_ecp_status=meta["ecp"]["status"],
            schema_dialect=validation["schema"]["dialect"],
            governance_enabled=gov["artifact_lifecycle"]["enabled"],
            runtime_enabled=runtime["execution_model"]["enabled"],
        )


class KernelLoader:
    def __init__(self, manifest_path: str | Path = "lep.yaml") -> None:
        self._manifest_path = Path(manifest_path)
        self._config: KernelConfig | None = None
        self._loaded = False

    def load(self) -> KernelConfig:
        if self._loaded:
            assert self._config is not None
            return self._config

        manifest_path = self._manifest_path.resolve()
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")

        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)

        self._config = KernelConfig.from_manifest(manifest)
        self._loaded = True
        return self._config

    @property
    def config(self) -> KernelConfig:
        if self._config is None:
            raise RuntimeError("Kernel not loaded. Call load() first.")
        return self._config

    @property
    def loaded(self) -> bool:
        return self._loaded
