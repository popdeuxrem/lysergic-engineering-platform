from __future__ import annotations

from typing import Any

from extensions.ecp.graph import ECPEntity, GraphValidationResult
from extensions.sdk.manifest import ExtensionManifest


class Tier1Validator:
    def __init__(self) -> None:
        self._schema_validator: Any = None
        self._entity_schema: dict[str, Any] = {}
        self._relationship_schema: dict[str, Any] = {}
        self._reference_schema: dict[str, Any] = {}

    def set_validator(self, validator: Any) -> None:
        self._schema_validator = validator

    def set_entity_schema(self, schema: dict[str, Any]) -> None:
        self._entity_schema = schema

    def set_relationship_schema(self, schema: dict[str, Any]) -> None:
        self._relationship_schema = schema

    def set_reference_schema(self, schema: dict[str, Any]) -> None:
        self._reference_schema = schema

    def validate_entity(self, entity: ECPEntity) -> GraphValidationResult:
        errors: list[str] = []
        if not entity.entity_id:
            errors.append("entity_id is required")
        if not entity.entity_type:
            errors.append("entity_type is required")
        if self._schema_validator and self._entity_schema:
            vr = self._schema_validator.validate(self._entity_schema, {"name": entity.name, "entity_type": entity.entity_type})
            if hasattr(vr, "valid") and not vr.valid:
                errors.extend(getattr(vr, "errors", ()))
        return GraphValidationResult(valid=len(errors) == 0, errors=tuple(errors))

    def validate_relationship(self, source_type: str | None = None, target_type: str | None = None) -> GraphValidationResult:
        return GraphValidationResult(valid=True, errors=())

    def validate_manifest(self, manifest: ExtensionManifest) -> GraphValidationResult:
        errors: list[str] = []
        if not manifest.extension_id:
            errors.append("extension_id is required")
        if manifest.extension_id != "ecp":
            errors.append(f"Expected extension_id 'ecp', got '{manifest.extension_id}'")
        return GraphValidationResult(valid=len(errors) == 0, errors=tuple(errors))
