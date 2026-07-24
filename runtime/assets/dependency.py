from __future__ import annotations


class DependencyGraphNode:
    def __init__(self, asset_id: str) -> None:
        self.asset_id = asset_id
        self.dependencies: set[str] = set()

    def add_dependency(self, dep_id: str) -> None:
        self.dependencies.add(dep_id)


class AssetDependencyGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, DependencyGraphNode] = {}

    def register(self, asset_id: str, dependencies: tuple[str, ...] = ()) -> None:
        if asset_id not in self._nodes:
            self._nodes[asset_id] = DependencyGraphNode(asset_id)
        for dep_id in dependencies:
            self._nodes[asset_id].add_dependency(dep_id)
            if dep_id not in self._nodes:
                self._nodes[dep_id] = DependencyGraphNode(dep_id)

    def resolve_order(self) -> list[str]:
        resolved: list[str] = []
        in_progress: set[str] = set()

        def visit(node: str) -> None:
            if node in resolved:
                return
            if node in in_progress:
                from runtime.assets.exceptions import DependencyCycleError
                raise DependencyCycleError(node)
            if node not in self._nodes:
                return
            in_progress.add(node)
            for dep in self._nodes[node].dependencies:
                visit(dep)
            in_progress.remove(node)
            if node not in resolved:
                resolved.append(node)

        for node in list(self._nodes):
            visit(node)
        return resolved

    def dependencies_of(self, asset_id: str) -> set[str]:
        node = self._nodes.get(asset_id)
        return set(node.dependencies) if node else set()

    def dependents_of(self, asset_id: str) -> set[str]:
        return {nid for nid, node in self._nodes.items() if asset_id in node.dependencies}

    def remove(self, asset_id: str) -> bool:
        if asset_id in self._nodes:
            del self._nodes[asset_id]
            for node in self._nodes.values():
                node.dependencies.discard(asset_id)
            return True
        return False

    @property
    def graph(self) -> dict[str, set[str]]:
        return {nid: set(node.dependencies) for nid, node in self._nodes.items()}
