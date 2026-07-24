from typing import Any

from runtime.api.validation import ValidationAPI
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
        return ValidationResult.ok() if "$schema" in schema else ValidationResult.fail(errors=("Missing $schema",))


def _make_api() -> ValidationAPI:
    from runtime.kernel.lifecycle import LifecycleManager
    from runtime.services.events import EventBus
    from runtime.services.health import HealthService
    from runtime.services.manager import ServiceManager
    from runtime.services.registry import ServiceRegistry
    from runtime.services.resolver import DependencyResolver
    m = ServiceManager(registry=ServiceRegistry(), resolver=DependencyResolver(), lifecycle=LifecycleManager(), health=HealthService(), event_bus=EventBus())
    return ValidationAPI(m)


def test_no_validator() -> None:
    api = _make_api()
    assert api.is_validator_set() is False
    assert api.dialect is None


def test_validate_without_validator() -> None:
    api = _make_api()
    r = api.validate_schema({"$schema": "x"}, {})
    assert r.valid is False


def test_set_validator() -> None:
    api = _make_api()
    api.set_validator(FakeValidator())
    assert api.is_validator_set() is True


def test_validate_schema() -> None:
    api = _make_api()
    api.set_validator(FakeValidator())
    r = api.validate_schema({"$schema": "x"}, {})
    assert r.valid is True


def test_validate_contract() -> None:
    api = _make_api()
    api.set_validator(FakeValidator())
    r = api.validate_contract({"$schema": "x"}, {})
    assert r.valid is True


def test_validate_profile() -> None:
    api = _make_api()
    api.set_validator(FakeValidator())
    r = api.validate_profile({"$schema": "x"}, {})
    assert r.valid is True


def test_aggregated_report() -> None:
    api = _make_api()
    api.set_validator(FakeValidator())
    checks: list[tuple[str, dict[str, object], dict[str, object]]] = [("schema", {"$schema": "x"}, {}), ("contract", {}, {})]
    r = api.aggregated_report(checks)
    assert r["all_valid"] is False
    assert r["checks"] == 2


def test_shutdown_clears() -> None:
    api = _make_api()
    api.set_validator(FakeValidator())
    api.shutdown()
    assert api.is_validator_set() is False
