from runtime.assets.dependency import AssetDependencyGraph


def test_empty_graph() -> None:
    g = AssetDependencyGraph()
    assert g.resolve_order() == []


def test_single_node() -> None:
    g = AssetDependencyGraph()
    g.register("ast-1")
    assert g.resolve_order() == ["ast-1"]


def test_linear_dependency() -> None:
    g = AssetDependencyGraph()
    g.register("main", ("dep",))
    g.register("dep")
    order = g.resolve_order()
    assert order.index("dep") < order.index("main")


def test_circular_dependency_raises() -> None:
    g = AssetDependencyGraph()
    g.register("a", ("b",))
    g.register("b", ("a",))
    try:
        g.resolve_order()
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_dependencies_of() -> None:
    g = AssetDependencyGraph()
    g.register("a", ("b", "c"))
    assert g.dependencies_of("a") == {"b", "c"}
    assert g.dependencies_of("b") == set()


def test_dependents_of() -> None:
    g = AssetDependencyGraph()
    g.register("a", ("b",))
    assert g.dependents_of("b") == {"a"}


def test_remove() -> None:
    g = AssetDependencyGraph()
    g.register("a", ("b",))
    assert g.remove("a") is True
    assert "a" not in g.graph


def test_graph_property() -> None:
    g = AssetDependencyGraph()
    g.register("a", ("b",))
    assert "b" in g.graph["a"]
