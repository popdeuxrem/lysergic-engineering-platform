from __future__ import annotations

from typing import Any, Protocol

from runtime.services.events import Event
from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceStatus


class DiagnosticsAPIProtocol(Protocol):
    def snapshot(self) -> dict[str, Any]: ...

    def record_error(self, source: str, message: str) -> None: ...

    def clear_errors(self) -> None: ...

    @property
    def service_count(self) -> int: ...

    def list_service_ids(self) -> tuple[str, ...]: ...

    def is_healthy(self) -> bool: ...


class DiagnosticsAPI:
    service_id = "api.diagnostics"
    dependencies: tuple[str, ...] = ()

    def __init__(self, manager: ServiceManager) -> None:
        self._manager = manager

    @property
    def status(self) -> ServiceStatus:
        return ServiceStatus.READY

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def snapshot(self) -> dict[str, Any]:
        report = self._manager.health_report()
        return {
            "health": {
                "overall": report.overall.value,
                "ready": report.ready_count,
                "total": report.total_count,
            },
            "services": {
                "registered": list(self._manager.registry.definitions.keys()),
                "instances": list(self._manager.registry.instances.keys()),
                "count": len(self._manager.registry),
            },
            "lifecycle": self._manager.lifecycle.state.value,
            "ready": self._manager.is_ready(),
        }

    def record_error(self, source: str, message: str) -> None:
        self._manager.event_bus.publish(Event(
            event_type="diagnostics.error",
            payload={"source": source, "message": message},
            source=source,
        ))

    def clear_errors(self) -> None:
        pass

    @property
    def service_count(self) -> int:
        return len(self._manager.registry)

    def list_service_ids(self) -> tuple[str, ...]:
        return tuple(self._manager.registry.definitions.keys())

    def is_healthy(self) -> bool:
        return self._manager.is_ready()


def create_diagnostics_api(manager: ServiceManager) -> ServiceDefinition:
    return ServiceDefinition(
        service_id="api.diagnostics",
        factory=lambda: DiagnosticsAPI(manager),
    )
