from __future__ import annotations

from extensions.ecp.graph import GraphValidationResult
from extensions.ecp.graph.entities import EntityRegistry
from extensions.ecp.graph.references import ReferenceResolver
from extensions.ecp.graph.relationships import RelationshipRegistry


class GraphValidator:
    def __init__(self, entities: EntityRegistry, relationships: RelationshipRegistry, references: ReferenceResolver) -> None:
        self._entities = entities
        self._relationships = relationships
        self._references = references

    def validate_all(self) -> GraphValidationResult:
        all_errors: list[str] = []
        all_warnings: list[str] = []

        entity_result = self._entities.validate()
        all_errors.extend(entity_result.errors)
        all_warnings.extend(entity_result.warnings)

        entity_ids = {e.entity_id for e in self._entities.list()}
        rel_result = self._relationships.validate(entity_ids)
        all_errors.extend(rel_result.errors)
        all_warnings.extend(rel_result.warnings)

        available_targets = {(e.entity_type, e.entity_id) for e in self._entities.list()}
        ref_result = self._references.validate(available_targets)
        all_errors.extend(ref_result.errors)
        all_warnings.extend(ref_result.warnings)

        dep_result = self._validate_acyclic()
        all_errors.extend(dep_result.errors)

        return GraphValidationResult(valid=len(all_errors) == 0, errors=tuple(all_errors), warnings=tuple(all_warnings))

    def _validate_acyclic(self) -> GraphValidationResult:
        graph: dict[str, list[str]] = {}
        for rel in self._relationships.list():
            graph.setdefault(rel.source_id, []).append(rel.target_id)
            graph.setdefault(rel.target_id, [])

        visited: set[str] = set()
        in_progress: set[str] = set()

        def visit(node: str) -> str | None:
            if node in in_progress:
                return node
            if node in visited:
                return None
            if node not in graph:
                return None
            in_progress.add(node)
            for dep in graph[node]:
                result = visit(dep)
                if result:
                    return result
            in_progress.remove(node)
            visited.add(node)
            return None

        errors: list[str] = []
        for node in graph:
            result = visit(node)
            if result:
                errors.append(f"Cycle detected involving entity: {result}")
                break

        return GraphValidationResult(valid=len(errors) == 0, errors=tuple(errors))
