from __future__ import annotations

from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus
from runtime.validator.interface import SchemaValidator, ValidationResult


class ValidationAPIProtocol(Protocol):
    def validate(self, schema: dict[str, Any], instance: Any) -> ValidationResult: ...

    def set_validator(self, validator: SchemaValidator) -> None: ...

    @property
    def dialect(self) -> str | None: ...

    def is_validator_set(self) -> bool: ...


class ValidationAPI:
    service_id = "api.validation"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._validator: SchemaValidator | None = None

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY if self._validator is not None else ServiceStatus.PENDING

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        self._validator = None

    def validate(self, schema: dict[str, Any], instance: Any) -> ValidationResult:
        if self._validator is None:
            return ValidationResult.fail(errors=("No validator configured",))
        return self._validator.validate(schema, instance)

    def set_validator(self, validator: SchemaValidator) -> None:
        self._validator = validator

    @property
    def dialect(self) -> str | None:
        if self._validator is None:
            return None
        return self._validator.dialect

    def is_validator_set(self) -> bool:
        return self._validator is not None


def create_validation_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(
        service_id="api.validation",
        factory=lambda: ValidationAPI(manager),
    )
