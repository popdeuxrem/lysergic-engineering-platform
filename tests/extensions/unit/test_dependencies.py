from extensions.sdk.dependencies import DependencyGraph, DependencyResolver


def test_empty_graph() -> None:
    g = DependencyGraph()
    assert g.resolve_order() == []


def test_single_node() -> None:
    g = DependencyGraph()
    g.add("a", [])
    assert g.resolve_order() == ["a"]


def test_linear_dependency() -> None:
    g = DependencyGraph()
    g.add("a", ["b"])
    g.add("b", [])
    order = g.resolve_order()
    assert order.index("b") < order.index("a")


def test_diamond_dependency() -> None:
    g = DependencyGraph()
    g.add("a", ["b", "c"])
    g.add("b", ["d"])
    g.add("c", ["d"])
    g.add("d", [])
    order = g.resolve_order()
    assert order.index("d") < order.index("b")
    assert order.index("d") < order.index("c")
    assert order.index("b") < order.index("a")
    assert order.index("c") < order.index("a")


def test_circular_dependency_raises() -> None:
    g = DependencyGraph()
    g.add("a", ["b"])
    g.add("b", ["a"])
    try:
        g.resolve_order()
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_reverse_order() -> None:
    g = DependencyGraph()
    g.add("a", ["b"])
    g.add("b", [])
    forward = g.resolve_order()
    reverse = g.reverse_order()
    assert forward == list(reversed(reverse))


def test_dependencies_of() -> None:
    g = DependencyGraph()
    g.add("a", ["b", "c"])
    g.add("b", [])
    g.add("c", [])
    assert g.dependencies_of("a") == {"b", "c"}
    assert g.dependencies_of("b") == set()


def test_dependents_of() -> None:
    g = DependencyGraph()
    g.add("a", ["b"])
    g.add("b", [])
    assert g.dependents_of("b") == {"a"}
    assert g.dependents_of("a") == set()


def test_graph_property() -> None:
    g = DependencyGraph()
    g.add("a", ["b"])
    assert g.graph == {"a": {"b"}, "b": set()}


def test_graph_add_auto_creates_missing_nodes() -> None:
    g = DependencyGraph()
    g.add("a", ["b"])
    assert "b" in g.graph


def test_resolver_with_optional() -> None:
    r = DependencyResolver()
    r.declare("a", ["b"], optional=["c"])
    r.declare("b", [])
    order = r.resolve()
    assert "b" in order
    assert "a" in order
    assert r.is_optional("c") is True
    assert r.is_optional("a") is False
