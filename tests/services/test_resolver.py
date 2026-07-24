from runtime.services.registry import ServiceDefinition
from runtime.services.resolver import DependencyResolver


def test_empty_graph() -> None:
    resolver = DependencyResolver()
    assert resolver.resolve_order() == []


def test_single_service() -> None:
    resolver = DependencyResolver()
    resolver.build_graph([ServiceDefinition(service_id="a")])
    assert resolver.resolve_order() == ["a"]


def test_linear_dependency() -> None:
    resolver = DependencyResolver()
    resolver.build_graph([
        ServiceDefinition(service_id="a", dependencies=("b",)),
        ServiceDefinition(service_id="b"),
    ])
    order = resolver.resolve_order()
    assert order.index("b") < order.index("a")


def test_diamond_dependency() -> None:
    resolver = DependencyResolver()
    resolver.build_graph([
        ServiceDefinition(service_id="a", dependencies=("b", "c")),
        ServiceDefinition(service_id="b", dependencies=("d",)),
        ServiceDefinition(service_id="c", dependencies=("d",)),
        ServiceDefinition(service_id="d"),
    ])
    order = resolver.resolve_order()
    assert order.index("d") < order.index("b")
    assert order.index("d") < order.index("c")
    assert order.index("b") < order.index("a")
    assert order.index("c") < order.index("a")


def test_circular_dependency_raises() -> None:
    resolver = DependencyResolver()
    resolver.build_graph([
        ServiceDefinition(service_id="a", dependencies=("b",)),
        ServiceDefinition(service_id="b", dependencies=("a",)),
    ])
    try:
        resolver.resolve_order()
        assert False, "Expected ValueError for circular dependency"
    except ValueError:
        pass


def test_reverse_order() -> None:
    resolver = DependencyResolver()
    resolver.build_graph([
        ServiceDefinition(service_id="a", dependencies=("b",)),
        ServiceDefinition(service_id="b"),
    ])
    forward = resolver.resolve_order()
    reverse = resolver.reverse_order()
    assert forward == list(reversed(reverse))


def test_dependencies_of() -> None:
    resolver = DependencyResolver()
    resolver.build_graph([
        ServiceDefinition(service_id="a", dependencies=("b", "c")),
        ServiceDefinition(service_id="b"),
        ServiceDefinition(service_id="c"),
    ])
    assert resolver.dependencies_of("a") == {"b", "c"}
    assert resolver.dependencies_of("b") == set()


def test_dependents_of() -> None:
    resolver = DependencyResolver()
    resolver.build_graph([
        ServiceDefinition(service_id="a", dependencies=("b",)),
        ServiceDefinition(service_id="b"),
    ])
    assert resolver.dependents_of("b") == {"a"}
    assert resolver.dependents_of("a") == set()


def test_graph_property() -> None:
    resolver = DependencyResolver()
    resolver.build_graph([
        ServiceDefinition(service_id="x", dependencies=("y",)),
        ServiceDefinition(service_id="y"),
    ])
    g = resolver.graph
    assert g["x"] == {"y"}
    assert g["y"] == set()
