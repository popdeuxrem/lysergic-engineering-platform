from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Protocol

from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


class RuntimeAPIProtocol(Protocol):
    def platform_name(self) -> str: ...
    def platform_version(self) -> str: ...
    def architecture_id(self) -> str: ...
    def architecture_status(self) -> str: ...
    def schema_dialect(self) -> str: ...
    def service_ids(self) -> tuple[str, ...]: ...
    def service_count(self) -> int: ...
    def is_governance_enabled(self) -> bool: ...
    def runtime_status(self) -> dict[str, Any]: ...
    def uptime(self) -> str: ...
    def summary(self) -> dict[str, Any]: ...


class RuntimeAPI:
    service_id = "api.runtime"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager
        self._started_at: datetime | None = None

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY if self._manager.is_ready() else ServiceStatus.PENDING

    def initialize(self) -> None:
        self._started_at = datetime.now(UTC)

    def shutdown(self) -> None:
        self._started_at = None

    def platform_name(self) -> str:
        return "Lysergic Engineering Platform"

    def platform_version(self) -> str:
        return "0.1.0"

    def architecture_id(self) -> str:
        return "LEP-ARCH-v0.1.0"

    def architecture_status(self) -> str:
        return "frozen"

    def schema_dialect(self) -> str:
        return "draft2020-12"

    def service_ids(self) -> tuple[str, ...]:
        return tuple(self._manager.registry.definitions.keys())

    def service_count(self) -> int:
        return len(self._manager.registry)

    def is_governance_enabled(self) -> bool:
        return True

    def runtime_status(self) -> dict[str, Any]:
        report = self._manager.health_report()
        return {
            "ready": self._manager.is_ready(),
            "health": report.overall.value,
            "lifecycle": self._manager.lifecycle.state.value,
            "started_at": self._started_at.isoformat() if self._started_at else None,
        }

    def uptime(self) -> str:
        if self._started_at is None:
            return "not started"
        delta = datetime.now(UTC) - self._started_at
        return f"{delta.seconds // 3600}h {(delta.seconds // 60) % 60}m"

    def summary(self) -> dict[str, Any]:
        return {
            "platform": self.platform_name(),
            "version": self.platform_version(),
            "architecture": self.architecture_id(),
            "architecture_status": self.architecture_status(),
            "schema_dialect": self.schema_dialect(),
            "governance": self.is_governance_enabled(),
            "services": self.service_count(),
            "ready": self._manager.is_ready(),
        }


def create_runtime_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(service_id="api.runtime", factory=lambda: RuntimeAPI(manager))
