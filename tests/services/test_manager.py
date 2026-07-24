from runtime.services.manager import ServiceManager
from runtime.services.registry import ServiceDefinition, ServiceRegistry, ServiceStatus


class TrackedService:
    def __init__(self, sid: str, deps: tuple[str, ...] = ()) -> None:
        self.service_id = sid
        self.dependencies = deps
        self._status = ServiceStatus.PENDING
        self.initialize_called = 0
        self.shutdown_called = 0

    def initialize(self) -> None:
        self.initialize_called += 1
        self._status = ServiceStatus.READY

    def shutdown(self) -> None:
        self.shutdown_called += 1
        self._status = ServiceStatus.STOPPED

    @property
    def status(self) -> ServiceStatus:
        return self._status


def test_manager_initialize_services() -> None:
    registry = ServiceRegistry()
    manager = ServiceManager(registry)

    svc = TrackedService("test-svc")
    registry.register(ServiceDefinition(service_id="test-svc", factory=lambda: svc))
    manager.initialize()

    assert svc.initialize_called == 1
    assert manager.is_ready() is True


def test_manager_initialize_idempotent() -> None:
    registry = ServiceRegistry()
    manager = ServiceManager(registry)
    svc = TrackedService("idempotent")
    registry.register(ServiceDefinition(service_id="idempotent", factory=lambda: svc))

    manager.initialize()
    manager.initialize()

    assert svc.initialize_called == 1


def test_manager_respects_dependency_order() -> None:
    registry = ServiceRegistry()
    manager = ServiceManager(registry)
    order: list[str] = []

    class OrderedService:
        def __init__(self, sid: str, deps: tuple[str, ...] = ()) -> None:
            self.service_id = sid
            self.dependencies = deps
            self._status = ServiceStatus.PENDING

        def initialize(self) -> None:
            order.append(self.service_id)
            self._status = ServiceStatus.READY

        def shutdown(self) -> None:
            self._status = ServiceStatus.STOPPED

        @property
        def status(self) -> ServiceStatus:
            return self._status

    registry.register(ServiceDefinition(service_id="dep", factory=lambda: OrderedService("dep")))
    registry.register(ServiceDefinition(service_id="main", factory=lambda: OrderedService("main", deps=("dep",)), dependencies=("dep",)))
    manager.initialize()

    assert order == ["dep", "main"]


def test_manager_reverse_shutdown_order() -> None:
    registry = ServiceRegistry()
    manager = ServiceManager(registry)
    shutdown_order: list[str] = []

    class ShutdownService:
        def __init__(self, sid: str, deps: tuple[str, ...] = ()) -> None:
            self.service_id = sid
            self.dependencies = deps
            self._status = ServiceStatus.PENDING

        def initialize(self) -> None:
            self._status = ServiceStatus.READY

        def shutdown(self) -> None:
            shutdown_order.append(self.service_id)
            self._status = ServiceStatus.STOPPED

        @property
        def status(self) -> ServiceStatus:
            return self._status

    registry.register(ServiceDefinition(service_id="dep", factory=lambda: ShutdownService("dep")))
    registry.register(ServiceDefinition(service_id="main", factory=lambda: ShutdownService("main", deps=("dep",)), dependencies=("dep",)))
    manager.initialize()
    manager.shutdown()

    assert shutdown_order == ["main", "dep"]


def test_manager_health_report() -> None:
    registry = ServiceRegistry()
    manager = ServiceManager(registry)
    svc = TrackedService("healthy")
    registry.register(ServiceDefinition(service_id="healthy", factory=lambda: svc))
    manager.initialize()

    report = manager.health_report()
    assert report.ready_count == 1
    assert report.total_count == 1


def test_manager_event_publishing() -> None:
    registry = ServiceRegistry()
    manager = ServiceManager(registry)
    svc = TrackedService("eventful")
    registry.register(ServiceDefinition(service_id="eventful", factory=lambda: svc))

    ready_events: list[str] = []
    manager.event_bus.subscribe("service.eventful.ready", lambda e: ready_events.append(e.event_type))
    manager.initialize()

    assert "service.eventful.ready" in ready_events
