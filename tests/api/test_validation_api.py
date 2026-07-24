from typing import Any

from runtime.api.validation import ValidationAPI
from runtime.kernel.lifecycle import LifecycleManager
from runtime.services.events import EventBus
from runtime.services.health import HealthService
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceRegistry
from runtime.services.resolver import DependencyResolver
from runtime.validator.interface import ValidationResult


class FakeValidator:
    def __init__(self, dialect: str = "draft2020-12") -> None:
        self._dialect = dialect

    @property
    def dialect(self) -> str:
        return self._dialect

    def supports_dialect(self, dialect: str) -> bool:
        return dialect == self._dialect

    def validate(self, schema: dict[str, Any], instance: Any) -> ValidationResult:
        if "$schema" in schema:
            return ValidationResult.ok()
        return ValidationResult.fail(errors=("Missing $schema",))


def _make_manager() -> ServiceManager:
    return ServiceManager(
        registry=ServiceRegistry(),
        resolver=DependencyResolver(),
        lifecycle=LifecycleManager(),
        health=HealthService(),
        event_bus=EventBus(),
    )


def test_validation_no_validator() -> None:
    api = ValidationAPI(_make_manager())
    assert api.is_validator_set() is False
    assert api.dialect is None


def test_validation_validate_without_validator() -> None:
    api = ValidationAPI(_make_manager())
    result = api.validate({"$schema": "x"}, {})
    assert result.valid is False
    assert "No validator configured" in result.errors


def test_validation_set_validator() -> None:
    api = ValidationAPI(_make_manager())
    validator = FakeValidator()
    api.set_validator(validator)
    assert api.is_validator_set() is True
    assert api.dialect == "draft2020-12"


def test_validation_validate_ok() -> None:
    api = ValidationAPI(_make_manager())
    api.set_validator(FakeValidator())
    result = api.validate({"$schema": "https://json-schema.org/draft/2020-12/schema"}, {})
    assert result.valid is True


def test_validation_validate_fail() -> None:
    api = ValidationAPI(_make_manager())
    api.set_validator(FakeValidator())
    result = api.validate({"title": "No schema"}, {})
    assert result.valid is False


def test_validation_shutdown_clears() -> None:
    api = ValidationAPI(_make_manager())
    api.set_validator(FakeValidator())
    api.shutdown()
    assert api.is_validator_set() is False
