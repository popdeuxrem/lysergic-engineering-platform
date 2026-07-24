from __future__ import annotations

from typing import Any

from runtime.validator.interface import SchemaValidator, ValidationResult
from runtime.workflows.model import WorkflowDefinition


class WorkflowValidator:
    def __init__(self) -> None:
        self._schema_validator: SchemaValidator | None = None
        self._workflow_schema: dict[str, Any] = {}
        self._step_schema: dict[str, Any] = {}

    def set_validator(self, validator: SchemaValidator) -> None:
        self._schema_validator = validator

    def set_workflow_schema(self, schema: dict[str, Any]) -> None:
        self._workflow_schema = schema

    def set_step_schema(self, schema: dict[str, Any]) -> None:
        self._step_schema = schema

    def validate_tier1(self, definition: WorkflowDefinition) -> ValidationResult:
        errors: list[str] = []
        if not definition.workflow_id:
            errors.append("workflow_id is required")
        if not definition.name:
            errors.append("name is required")
        if not definition.steps:
            errors.append("at least one step is required")
        for step in definition.steps:
            if not step.step_id:
                errors.append("each step must have a step_id")
        if self._schema_validator and self._workflow_schema:
            vr = self._schema_validator.validate(self._workflow_schema, {"name": definition.name, "version": definition.version})
            if not vr.valid:
                errors.extend(vr.errors)
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()

    def validate_tier2(self, definition: WorkflowDefinition) -> ValidationResult:
        errors: list[str] = []
        step_ids = [s.step_id for s in definition.steps]
        if len(step_ids) != len(set(step_ids)):
            errors.append("duplicate step_ids detected")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()
