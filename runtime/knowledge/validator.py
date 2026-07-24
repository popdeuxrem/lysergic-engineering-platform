from __future__ import annotations

from typing import Any

from runtime.knowledge.model import KnowledgeItem
from runtime.validator.interface import SchemaValidator, ValidationResult


class KnowledgeValidator:
    def __init__(self) -> None:
        self._schema_validator: SchemaValidator | None = None
        self._knowledge_schema: dict[str, Any] = {}

    def set_validator(self, validator: SchemaValidator) -> None:
        self._schema_validator = validator

    def set_knowledge_schema(self, schema: dict[str, Any]) -> None:
        self._knowledge_schema = schema

    def validate_tier1(self, item: KnowledgeItem) -> ValidationResult:
        errors: list[str] = []
        if not item.knowledge_id:
            errors.append("knowledge_id is required")
        if not item.title:
            errors.append("title is required")
        if not item.kind:
            errors.append("kind is required")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()

    def validate_tier2(self, item: KnowledgeItem) -> ValidationResult:
        errors: list[str] = []
        if item.metadata and not item.metadata.author:
            pass
        ref_ids = [r.ref_id for r in item.references]
        if len(ref_ids) != len(set(ref_ids)):
            errors.append("Duplicate reference IDs")
        if errors:
            return ValidationResult.fail(errors=tuple(errors))
        return ValidationResult.ok()
