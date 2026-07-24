from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from extensions.sdk.capabilities import CapabilityRegistry
from extensions.sdk.compatibility import CompatibilityChecker
from extensions.sdk.dependencies import DependencyResolver
from extensions.sdk.manifest import (
    ExtensionManifest,
    ManifestValidationError,
)


class ValidationTier(Enum):
    TIER_1 = "manifest_schema"
    TIER_2 = "dependency_graph"


@dataclass
class ValidationResult:
    tier: ValidationTier
    passed: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


class ValidationEngine:
    def __init__(self, checker: CompatibilityChecker) -> None:
        self._checker = checker
        self._results: list[ValidationResult] = []

    def validate_manifest(self, manifest: ExtensionManifest) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not manifest.extension_id:
            errors.append("extension_id is required")
        if not manifest.name:
            errors.append("name is required")
        if not manifest.version:
            errors.append("version is required")
        if not manifest.entry_point:
            warnings.append("entry_point is not set")
        if manifest.min_sdk_version:
            compatible, msg = self._checker.check_sdk_compatibility(manifest.min_sdk_version, manifest.max_sdk_version)
            if not compatible:
                warnings.append(msg)

        result = ValidationResult(
            tier=ValidationTier.TIER_1,
            passed=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
        self._results.append(result)

        if not result.passed:
            raise ManifestValidationError("Manifest validation failed", errors=result.errors)

        return result

    def validate_dependencies(
        self,
        resolver: DependencyResolver,
        registry: Any,
        capability_registry: CapabilityRegistry,
    ) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        try:
            resolver.resolve()
        except ValueError as exc:
            errors.append(str(exc))
            result = ValidationResult(tier=ValidationTier.TIER_2, passed=False, errors=tuple(errors))
            self._results.append(result)
            return result

        result = ValidationResult(
            tier=ValidationTier.TIER_2,
            passed=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
        self._results.append(result)
        return result

    def clear(self) -> None:
        self._results.clear()

    @property
    def results(self) -> tuple[ValidationResult, ...]:
        return tuple(self._results)
