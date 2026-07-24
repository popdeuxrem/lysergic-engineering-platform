from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class HealthStatus(Enum):
    UNKNOWN = "unknown"
    READY = "ready"
    DEGRADED = "degraded"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass
class ServiceHealth:
    service_id: str
    status: HealthStatus = HealthStatus.UNKNOWN
    last_check: datetime = field(default_factory=lambda: datetime.now(UTC))
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthReport:
    overall: HealthStatus
    services: dict[str, ServiceHealth] = field(default_factory=dict)
    ready_count: int = 0
    total_count: int = 0
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def summary(self) -> str:
        return f"{self.ready_count}/{self.total_count} services ready — overall: {self.overall.value}"


class HealthService:
    def __init__(self) -> None:
        self._health: dict[str, ServiceHealth] = {}

    def register(self, service_id: str) -> None:
        if service_id not in self._health:
            self._health[service_id] = ServiceHealth(service_id=service_id)

    def report_ready(self, service_id: str, message: str = "") -> None:
        self._ensure(service_id)
        self._health[service_id].status = HealthStatus.READY
        self._health[service_id].last_check = datetime.now(UTC)
        self._health[service_id].message = message

    def report_degraded(self, service_id: str, message: str = "") -> None:
        self._ensure(service_id)
        self._health[service_id].status = HealthStatus.DEGRADED
        self._health[service_id].last_check = datetime.now(UTC)
        self._health[service_id].message = message

    def report_failure(self, service_id: str, message: str = "") -> None:
        self._ensure(service_id)
        self._health[service_id].status = HealthStatus.FAILED
        self._health[service_id].last_check = datetime.now(UTC)
        self._health[service_id].message = message

    def report_stopped(self, service_id: str, message: str = "") -> None:
        self._ensure(service_id)
        self._health[service_id].status = HealthStatus.STOPPED
        self._health[service_id].last_check = datetime.now(UTC)
        self._health[service_id].message = message

    def report(
        self,
    ) -> HealthReport:
        services = dict(self._health)
        counts = {s: 0 for s in HealthStatus}
        for h in services.values():
            counts[h.status] = counts.get(h.status, 0) + 1
        total = len(services)
        ready = counts.get(HealthStatus.READY, 0)

        if total == 0:
            overall = HealthStatus.UNKNOWN
        elif ready == total:
            overall = HealthStatus.READY
        elif counts.get(HealthStatus.FAILED, 0) > 0:
            overall = HealthStatus.FAILED
        else:
            overall = HealthStatus.DEGRADED

        return HealthReport(
            overall=overall,
            services=services,
            ready_count=ready,
            total_count=total,
        )

    def service_status(self, service_id: str) -> HealthStatus:
        if service_id not in self._health:
            return HealthStatus.UNKNOWN
        return self._health[service_id].status

    def all_ready(self) -> bool:
        report = self.report()
        return report.overall == HealthStatus.READY

    def _ensure(self, service_id: str) -> None:
        if service_id not in self._health:
            self._health[service_id] = ServiceHealth(service_id=service_id)
