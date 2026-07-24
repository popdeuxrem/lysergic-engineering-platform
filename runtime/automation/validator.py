from __future__ import annotations

from typing import Any

from runtime.automation.model import Automation
from runtime.validator.interface import SchemaValidator, ValidationResult


class AutomationValidator:
    def __init__(self) -> None:
        self._schema_validator: SchemaValidator | None = None
        self._automation_schema: dict[str, Any] = {}

    def set_validator(self, validator: SchemaValidator) -> None:
        self._schema_validator = validator

    def set_automation_schema(self, schema: dict[str, Any]) -> None:
        self._automation_schema = schema

    def validate_tier1(self, automation: Automation) -> ValidationResult:
        errors: list[str] = []
        if not automation.automation_id:
            errors.append("automation_id is required")
        if not automation.name:
            errors.append("name is required")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()

    def validate_tier2(self, automation: Automation) -> ValidationResult:
        errors: list[str] = []
        trigger_ids = [t.trigger_id for t in automation.triggers]
        if len(trigger_ids) != len(set(trigger_ids)):
            errors.append("Duplicate trigger IDs")
        action_ids = [a.action_id for a in automation.actions]
        if len(action_ids) != len(set(action_ids)):
            errors.append("Duplicate action IDs")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()
