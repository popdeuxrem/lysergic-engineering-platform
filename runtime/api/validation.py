from __future__ import annotations

from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus
from runtime.validator.interface import SchemaValidator, ValidationResult


class ValidationReport:
    def __init__(self) -> None:
        self.results: list[dict[str, Any]] = []

    def add(self, category: str, result: ValidationResult) -> None:
        self.results.append({"category": category, "valid": result.valid, "errors": list(result.errors), "warnings": list(result.warnings)})

    @property
    def all_valid(self) -> bool:
        return all(r["valid"] for r in self.results)

    def to_dict(self) -> dict[str, Any]:
        return {"all_valid": self.all_valid, "checks": len(self.results), "results": self.results}


class ValidationAPIProtocol(Protocol):
    def validate_schema(self, schema: dict[str, Any], instance: Any) -> ValidationResult: ...
    def validate_contract(self, contract: dict[str, Any], instance: Any) -> ValidationResult: ...
    def validate_profile(self, profile: dict[str, Any], instance: Any) -> ValidationResult: ...
    def aggregated_report(self, checks: list[tuple[str, dict[str, Any], Any]]) -> dict[str, Any]: ...
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

    def validate_schema(self, schema: dict[str, Any], instance: Any) -> ValidationResult:
        return self._validate(schema, instance)

    def validate_contract(self, contract: dict[str, Any], instance: Any) -> ValidationResult:
        return self._validate(contract, instance)

    def validate_profile(self, profile: dict[str, Any], instance: Any) -> ValidationResult:
        return self._validate(profile, instance)

    def aggregated_report(self, checks: list[tuple[str, dict[str, Any], Any]]) -> dict[str, Any]:
        report = ValidationReport()
        for category, schema, instance in checks:
            result = self._validate(schema, instance)
            report.add(category, result)
        return report.to_dict()

    def set_validator(self, validator: SchemaValidator) -> None:
        self._validator = validator

    @property
    def dialect(self) -> str | None:
        return None if self._validator is None else self._validator.dialect

    def is_validator_set(self) -> bool:
        return self._validator is not None

    def _validate(self, schema: dict[str, Any], instance: Any) -> ValidationResult:
        if self._validator is None:
            return ValidationResult.fail(errors=("No validator configured",))
        return self._validator.validate(schema, instance)


def create_validation_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(service_id="api.validation", factory=lambda: ValidationAPI(manager))
