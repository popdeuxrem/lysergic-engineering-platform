from __future__ import annotations

from extensions.ecp.graph import GraphValidationResult
from extensions.ecp.graph.entities import EntityRegistry
from extensions.ecp.graph.references import ReferenceResolver
from extensions.ecp.graph.relationships import RelationshipRegistry
from extensions.ecp.graph.validator import GraphValidator


class Tier2Validator:
    def __init__(self, entities: EntityRegistry, relationships: RelationshipRegistry, references: ReferenceResolver) -> None:
        self._graph = GraphValidator(entities, relationships, references)

    def validate_graph(self) -> GraphValidationResult:
        return self._graph.validate_all()

    def validate_semantic(self) -> GraphValidationResult:
        return GraphValidationResult(valid=True, errors=())
