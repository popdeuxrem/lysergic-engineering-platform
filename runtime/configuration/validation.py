from __future__ import annotations

from typing import Any

from runtime.validator.interface import SchemaValidator, ValidationResult


class ConfigValidator:
    def __init__(self) -> None:
        self._schemas: dict[str, dict[str, Any]] = {}
        self._validator: SchemaValidator | None = None

    def register_schema(self, key: str, schema: dict[str, Any]) -> None:
        self._schemas[key] = schema

    def set_validator(self, validator: SchemaValidator) -> None:
        self._validator = validator

    def validate(self, config: dict[str, Any]) -> ValidationResult:
        if self._validator is None:
            return ValidationResult.ok()
        for key, schema in self._schemas.items():
            value = self._get_nested(config, key)
            if value is not None:
                result = self._validator.validate(schema, value)
                if not result.valid:
                    return ValidationResult.fail(
                        errors=tuple(f"{key}: {e}" for e in result.errors),
                        warnings=result.warnings,
                    )
        return ValidationResult.ok()

    def validate_key(self, config: dict[str, Any], key: str) -> ValidationResult:
        if key not in self._schemas:
            return ValidationResult.ok()
        if self._validator is None:
            return ValidationResult.ok()
        value = self._get_nested(config, key)
        if value is None:
            return ValidationResult.fail(errors=(f"Required key '{key}' not found in config",))
        return self._validator.validate(self._schemas[key], value)

    def _get_nested(self, config: dict[str, Any], key: str) -> Any:
        keys = key.split(".")
        current: Any = config
        for k in keys:
            if not isinstance(current, dict):
                return None
            val = current.get(k)
            if val is None:
                return None
            current = val
        return current
