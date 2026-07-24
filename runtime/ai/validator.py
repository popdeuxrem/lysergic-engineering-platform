from __future__ import annotations

from typing import Any

from runtime.ai.model import Agent
from runtime.validator.interface import SchemaValidator, ValidationResult


class AIValidator:
    def __init__(self) -> None:
        self._schema_validator: SchemaValidator | None = None
        self._agent_schema: dict[str, Any] = {}

    def set_validator(self, validator: SchemaValidator) -> None:
        self._schema_validator = validator

    def set_agent_schema(self, schema: dict[str, Any]) -> None:
        self._agent_schema = schema

    def validate_tier1(self, agent: Agent) -> ValidationResult:
        errors: list[str] = []
        if not agent.agent_id:
            errors.append("agent_id is required")
        if not agent.name:
            errors.append("name is required")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()

    def validate_tier2(self, agent: Agent, available_tools: set[str]) -> ValidationResult:
        errors: list[str] = []
        cap_ids = [c.capability_id for c in agent.capabilities]
        if len(cap_ids) != len(set(cap_ids)):
            errors.append("Duplicate capability IDs")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()
