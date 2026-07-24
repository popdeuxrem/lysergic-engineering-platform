from __future__ import annotations

from collections.abc import Iterable


class DependencyGraph:
    def __init__(self) -> None:
        self._graph: dict[str, set[str]] = {}

    def add(self, node: str, dependencies: Iterable[str]) -> None:
        if node not in self._graph:
            self._graph[node] = set()
        for dep in dependencies:
            self._graph[node].add(dep)
            if dep not in self._graph:
                self._graph[dep] = set()

    def resolve_order(self) -> list[str]:
        resolved: list[str] = []
        in_progress: set[str] = set()

        def visit(node: str) -> None:
            if node in resolved:
                return
            if node in in_progress:
                raise ValueError(f"Circular dependency detected: {node}")
            if node not in self._graph:
                return
            in_progress.add(node)
            for dep in self._graph[node]:
                visit(dep)
            in_progress.remove(node)
            if node not in resolved:
                resolved.append(node)

        for node in list(self._graph):
            visit(node)
        return resolved

    def reverse_order(self) -> list[str]:
        return list(reversed(self.resolve_order()))

    def dependencies_of(self, node: str) -> set[str]:
        return self._graph.get(node, set())

    def dependents_of(self, node: str) -> set[str]:
        return {n for n, deps in self._graph.items() if node in deps}

    @property
    def graph(self) -> dict[str, set[str]]:
        return {k: set(v) for k, v in self._graph.items()}


class DependencyResolver:
    def __init__(self) -> None:
        self._graph = DependencyGraph()
        self._optional: set[str] = set()

    def declare(self, extension_id: str, dependencies: Iterable[str], optional: Iterable[str] = ()) -> None:
        self._graph.add(extension_id, dependencies)
        self._optional.update(optional)

    def resolve(self) -> list[str]:
        return self._graph.resolve_order()

    def resolve_with_optional(self) -> list[str]:
        return self.resolve()

    def is_optional(self, extension_id: str) -> bool:
        return extension_id in self._optional

    def dependencies_of(self, extension_id: str) -> set[str]:
        return self._graph.dependencies_of(extension_id)

    def dependents_of(self, extension_id: str) -> set[str]:
        return self._graph.dependents_of(extension_id)
