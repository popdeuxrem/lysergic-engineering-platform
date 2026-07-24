from __future__ import annotations

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

    def summary(self) -> dict[str, Any]: ...


class RuntimeAPI:
    service_id = "api.runtime"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY if self._manager.is_ready() else ServiceStatus.PENDING

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

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
    return ServiceDefinition(
        service_id="api.runtime",
        factory=lambda: RuntimeAPI(manager),
    )
