from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from runtime.services.health import HealthReport, HealthService
from runtime.services.registry import ServiceRegistry


@dataclass
class DiagnosticsSnapshot:
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    registry_size: int = 0
    registered_ids: tuple[str, ...] = ()
    instance_ids: tuple[str, ...] = ()
    health: HealthReport | None = None
    errors: tuple[dict[str, str], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "registry_size": self.registry_size,
            "registered_ids": list(self.registered_ids),
            "instance_ids": list(self.instance_ids),
            "health": {
                "overall": self.health.overall.value if self.health else "unknown",
                "ready": self.health.ready_count if self.health else 0,
                "total": self.health.total_count if self.health else 0,
            } if self.health else None,
            "errors": list(self.errors),
        }


class Diagnostics:
    def __init__(self, registry: ServiceRegistry, health: HealthService) -> None:
        self._registry = registry
        self._health = health
        self._errors: list[dict[str, str]] = []

    def record_error(self, source: str, message: str) -> None:
        self._errors.append({"source": source, "message": message, "timestamp": datetime.now(UTC).isoformat()})

    def snapshot(self) -> DiagnosticsSnapshot:
        return DiagnosticsSnapshot(
            registry_size=len(self._registry),
            registered_ids=tuple(self._registry.definitions.keys()),
            instance_ids=tuple(self._registry.instances.keys()),
            health=self._health.report(),
            errors=tuple(self._errors),
        )

    def clear_errors(self) -> None:
        self._errors.clear()
