from __future__ import annotations

from typing import Any

from runtime.assets.dependency import AssetDependencyGraph
from runtime.assets.metadata import AssetMetadata
from runtime.validator.interface import SchemaValidator


class AssetValidationResult:
    def __init__(self) -> None:
        self.tier1_errors: list[str] = []
        self.tier2_errors: list[str] = []
        self.warnings: list[str] = []

    @property
    def valid(self) -> bool:
        return len(self.tier1_errors) == 0 and len(self.tier2_errors) == 0

    def to_dict(self) -> dict[str, Any]:
        return {"valid": self.valid, "tier1_errors": self.tier1_errors, "tier2_errors": self.tier2_errors, "warnings": self.warnings}


class AssetValidator:
    def __init__(self) -> None:
        self._schema_validator: SchemaValidator | None = None
        self._metadata_schema: dict[str, Any] = {}
        self._asset_schema: dict[str, Any] = {}

    def set_schema_validator(self, validator: SchemaValidator) -> None:
        self._schema_validator = validator

    def set_metadata_schema(self, schema: dict[str, Any]) -> None:
        self._metadata_schema = schema

    def set_asset_schema(self, schema: dict[str, Any]) -> None:
        self._asset_schema = schema

    def validate(self, metadata: AssetMetadata) -> AssetValidationResult:
        result = AssetValidationResult()
        if self._schema_validator is None:
            return result
        if self._metadata_schema:
            vr = self._schema_validator.validate(self._metadata_schema, metadata.to_dict())
            if not vr.valid:
                result.tier1_errors.extend(vr.errors)
        if not metadata.asset_id:
            result.tier1_errors.append("asset_id is required")
        if not metadata.asset_type:
            result.tier1_errors.append("asset_type is required")
        if not metadata.version:
            result.tier1_errors.append("version is required")
        return result

    def validate_dependencies(self, graph: AssetDependencyGraph) -> AssetValidationResult:
        result = AssetValidationResult()
        try:
            graph.resolve_order()
        except Exception as e:  # noqa: BLE001
            result.tier2_errors.append(str(e))
        return result
