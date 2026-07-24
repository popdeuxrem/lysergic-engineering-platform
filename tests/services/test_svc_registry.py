from runtime.services.registry import ServiceDefinition, ServiceRegistry, ServiceStatus


class FakeService:
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


def test_register_definition() -> None:
    registry = ServiceRegistry()
    definition = ServiceDefinition(service_id="test", dependencies=("dep1",))
    registry.register(definition)
    assert "test" in registry
    assert len(registry) == 1


def test_register_duplicate_definition_raises() -> None:
    registry = ServiceRegistry()
    registry.register(ServiceDefinition(service_id="dup"))
    try:
        registry.register(ServiceDefinition(service_id="dup"))
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_register_instance() -> None:
    registry = ServiceRegistry()
    service = FakeService("instance-svc")
    registry.register_instance(service)
    assert registry.resolve("instance-svc") is service


def test_register_instance_duplicate_raises() -> None:
    registry = ServiceRegistry()
    registry.register_instance(FakeService("x"))
    try:
        registry.register_instance(FakeService("x"))
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_freeze_prevents_registration() -> None:
    registry = ServiceRegistry()
    registry.freeze()
    try:
        registry.register(ServiceDefinition(service_id="late"))
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass


def test_resolve_missing_raises() -> None:
    registry = ServiceRegistry()
    try:
        registry.resolve("nonexistent")
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_resolve_with_factory() -> None:
    registry = ServiceRegistry()
    registry.register(ServiceDefinition(service_id="factory-svc", factory=lambda: FakeService("factory-svc")))
    service = registry.resolve("factory-svc")
    assert service.service_id == "factory-svc"


def test_resolve_factory_singleton() -> None:
    registry = ServiceRegistry()
    registry.register(ServiceDefinition(service_id="singleton", factory=lambda: FakeService("singleton")))
    a = registry.resolve("singleton")
    b = registry.resolve("singleton")
    assert a is b


def test_definitions_property() -> None:
    registry = ServiceRegistry()
    registry.register(ServiceDefinition(service_id="a"))
    registry.register(ServiceDefinition(service_id="b"))
    assert set(registry.definitions.keys()) == {"a", "b"}
