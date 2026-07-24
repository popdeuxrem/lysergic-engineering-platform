from __future__ import annotations

from collections.abc import Callable

from runtime.kernel.lifecycle import LifecycleManager, LifecycleState
from runtime.services.events import Event, EventBus
from runtime.services.health import HealthReport, HealthService
from runtime.services.registry import ServiceDefinition, ServiceRegistry
from runtime.services.resolver import DependencyResolver


class ServiceManager:
    def __init__(
        self,
        registry: ServiceRegistry,
        resolver: DependencyResolver | None = None,
        lifecycle: LifecycleManager | None = None,
        health: HealthService | None = None,
        event_bus: EventBus | None = None,
    ) -> None:
        self._registry = registry
        self._resolver = resolver or DependencyResolver()
        self._lifecycle = lifecycle or LifecycleManager()
        self._health = health or HealthService()
        self._event_bus = event_bus or EventBus()
        self._initialized = False

    @property
    def registry(self) -> ServiceRegistry:
        return self._registry

    @property
    def lifecycle(self) -> LifecycleManager:
        return self._lifecycle

    @property
    def health(self) -> HealthService:
        return self._health

    @property
    def event_bus(self) -> EventBus:
        return self._event_bus

    def register(self, definition: ServiceDefinition) -> None:
        self._registry.register(definition)

    def initialize(self) -> None:
        if self._initialized:
            return
        definitions = list(self._registry.definitions.values())
        self._resolver.build_graph(definitions)
        init_order = self._resolver.resolve_order()

        self._lifecycle.add_start_hook(lambda: self._initialize_services(init_order))
        self._lifecycle.add_stop_hook(lambda: self._shutdown_services(init_order))
        self._lifecycle.start()
        self._initialized = True

    def _initialize_services(self, init_order: list[str]) -> None:
        for sid in init_order:
            try:
                service = self._registry.resolve(sid)
                service.initialize()
                self._health.report_ready(sid)
                self._event_bus.publish(Event(f"service.{sid}.ready", {"service_id": sid}))
            except Exception as exc:  # noqa: BLE001
                self._health.report_failure(sid, str(exc))
                self._event_bus.publish(Event(f"service.{sid}.failed", {"service_id": sid, "error": str(exc)}))

    def _shutdown_services(self, init_order: list[str]) -> None:
        for sid in reversed(init_order):
            try:
                service = self._registry.resolve(sid)
                service.shutdown()
                self._health.report_stopped(sid)
                self._event_bus.publish(Event(f"service.{sid}.stopped", {"service_id": sid}))
            except Exception as exc:  # noqa: BLE001
                self._event_bus.publish(Event(f"service.{sid}.shutdown_error", {"service_id": sid, "error": str(exc)}))

    def shutdown(self) -> None:
        if self._lifecycle.state not in (LifecycleState.READY, LifecycleState.CREATED):
            return
        self._lifecycle.stop()
        self._initialized = False

    def health_report(self) -> HealthReport:
        return self._health.report()

    def is_ready(self) -> bool:
        return self._lifecycle.is_ready() and self._health.all_ready()

    def add_start_hook(self, hook: Callable[[], None]) -> None:
        self._lifecycle.add_start_hook(hook)

    def add_stop_hook(self, hook: Callable[[], None]) -> None:
        self._lifecycle.add_stop_hook(hook)
