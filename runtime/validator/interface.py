from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @classmethod
    def ok(cls) -> ValidationResult:
        return cls(valid=True, errors=(), warnings=())

    @classmethod
    def fail(cls, errors: tuple[str, ...], warnings: tuple[str, ...] = ()) -> ValidationResult:
        return cls(valid=False, errors=errors, warnings=warnings)


@runtime_checkable
class SchemaValidator(Protocol):
    def validate(self, schema: dict[str, Any], instance: Any) -> ValidationResult: ...

    def supports_dialect(self, dialect: str) -> bool: ...

    @property
    def dialect(self) -> str: ...
