from typing import Any

from runtime.validator.interface import SchemaValidator, ValidationResult


class FakeValidator:
    def __init__(self, dialect: str = "draft2020-12") -> None:
        self._dialect = dialect
        self._called_with: list[tuple[dict[str, Any], Any]] = []

    def validate(self, schema: dict[str, Any], instance: Any) -> ValidationResult:
        self._called_with.append((schema, instance))
        is_valid = "$schema" in schema and schema["$schema"] is not None
        return ValidationResult.ok() if is_valid else ValidationResult.fail(errors=("Missing $schema",))

    def supports_dialect(self, dialect: str) -> bool:
        return dialect == self._dialect

    @property
    def dialect(self) -> str:
        return self._dialect


def test_validator_protocol_satisfied() -> None:
    validator: SchemaValidator = FakeValidator()
    assert isinstance(validator, SchemaValidator)


def test_validation_result_ok() -> None:
    result = ValidationResult.ok()
    assert result.valid is True
    assert result.errors == ()


def test_validation_result_fail() -> None:
    result = ValidationResult.fail(errors=("error1",))
    assert result.valid is False
    assert result.errors == ("error1",)


def test_validator_validate() -> None:
    validator = FakeValidator()
    result = validator.validate({"$schema": "https://json-schema.org/draft/2020-12/schema"}, {})
    assert result.valid is True


def test_validator_supports_dialect() -> None:
    validator = FakeValidator()
    assert validator.supports_dialect("draft2020-12") is True
    assert validator.supports_dialect("draft2019-09") is False


def test_validator_dialect_property() -> None:
    validator = FakeValidator("draft2020-12")
    assert validator.dialect == "draft2020-12"
