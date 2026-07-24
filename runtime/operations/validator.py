from __future__ import annotations

from typing import Any

from runtime.operations.model import EngineeringOperation
from runtime.validator.interface import SchemaValidator, ValidationResult


class OperationsValidator:
    def __init__(self) -> None:
        self._schema_validator: SchemaValidator | None = None
        self._op_schema: dict[str, Any] = {}

    def set_validator(self, validator: SchemaValidator) -> None:
        self._schema_validator = validator

    def set_op_schema(self, schema: dict[str, Any]) -> None:
        self._op_schema = schema

    def validate_tier1(self, op: EngineeringOperation) -> ValidationResult:
        errors: list[str] = []
        if not op.operation_id:
            errors.append("operation_id is required")
        if not op.name:
            errors.append("name is required")
        step_ids = [s.step_id for s in op.steps]
        if len(step_ids) != len(set(step_ids)):
            errors.append("Duplicate step IDs")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()

    def validate_tier2(self, op: EngineeringOperation) -> ValidationResult:
        errors: list[str] = []
        gate_ids = [g.gate_id for g in op.gates]
        if len(gate_ids) != len(set(gate_ids)):
            errors.append("Duplicate gate IDs")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()
