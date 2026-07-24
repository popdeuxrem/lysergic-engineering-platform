from runtime.configuration.validation import ConfigValidator
from runtime.validator.interface import ValidationResult


class FakeValidator:
    def __init__(self, should_pass: bool = True) -> None:
        self._should_pass = should_pass
    @property
    def dialect(self) -> str:
        return "draft2020-12"
    def supports_dialect(self, dialect: str) -> bool:
        return dialect == "draft2020-12"
    def validate(self, schema: dict[str, object], instance: object) -> ValidationResult:
        if self._should_pass:
            return ValidationResult.ok()
        return ValidationResult.fail(errors=("validation failed",))


def test_validate_no_validator() -> None:
    v = ConfigValidator()
    result = v.validate({"key": "val"})
    assert result.valid is True


def test_validate_with_validator_pass() -> None:
    v = ConfigValidator()
    v.set_validator(FakeValidator(should_pass=True))
    v.register_schema("app", {"type": "object"})
    result = v.validate({"app": {"name": "test"}})
    assert result.valid is True


def test_validate_with_validator_fail() -> None:
    v = ConfigValidator()
    v.set_validator(FakeValidator(should_pass=False))
    v.register_schema("app", {"type": "object"})
    result = v.validate({"app": {"name": "test"}})
    assert result.valid is False


def test_validate_key() -> None:
    v = ConfigValidator()
    v.set_validator(FakeValidator(should_pass=True))
    v.register_schema("app", {"type": "object"})
    result = v.validate_key({"app": {}}, "app")
    assert result.valid is True


def test_validate_key_missing() -> None:
    v = ConfigValidator()
    v.set_validator(FakeValidator(should_pass=True))
    v.register_schema("required.key", {"type": "string"})
    result = v.validate_key({}, "required.key")
    assert result.valid is False


def test_validate_key_no_schema() -> None:
    v = ConfigValidator()
    result = v.validate_key({"x": 1}, "x")
    assert result.valid is True
