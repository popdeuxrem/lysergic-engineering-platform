from __future__ import annotations

from collections.abc import Iterable

from runtime.services.registry import ServiceDefinition


class DependencyResolver:
    def __init__(self) -> None:
        self._graph: dict[str, set[str]] = {}

    def build_graph(self, definitions: Iterable[ServiceDefinition]) -> None:
        self._graph = {}
        for d in definitions:
            self._graph.setdefault(d.service_id, set())
            for dep in d.dependencies:
                if dep not in self._graph:
                    self._graph[dep] = set()
                self._graph[d.service_id].add(dep)

    def resolve_order(self) -> list[str]:
        visited: set[str] = set()
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
                visited.add(node)
                resolved.append(node)

        for node in list(self._graph):
            visit(node)

        return resolved

    def reverse_order(self) -> list[str]:
        return list(reversed(self.resolve_order()))

    def dependencies_of(self, service_id: str) -> set[str]:
        return self._graph.get(service_id, set())

    def dependents_of(self, service_id: str) -> set[str]:
        return {sid for sid, deps in self._graph.items() if service_id in deps}

    @property
    def graph(self) -> dict[str, set[str]]:
        return {k: set(v) for k, v in self._graph.items()}
