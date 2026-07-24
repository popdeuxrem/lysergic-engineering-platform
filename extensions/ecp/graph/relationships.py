from __future__ import annotations

from extensions.ecp.graph import ECPRelationship, GraphValidationResult


class RelationshipRegistry:
    def __init__(self) -> None:
        self._relationships: dict[str, ECPRelationship] = {}

    def create(self, relationship: ECPRelationship) -> ECPRelationship:
        if relationship.relationship_id in self._relationships:
            raise ValueError(f"Relationship already exists: {relationship.relationship_id}")
        self._relationships[relationship.relationship_id] = relationship
        return relationship

    def get(self, relationship_id: str) -> ECPRelationship | None:
        return self._relationships.get(relationship_id)

    def list(self) -> tuple[ECPRelationship, ...]:
        return tuple(self._relationships.values())

    def list_for_entity(self, entity_id: str) -> tuple[ECPRelationship, ...]:
        return tuple(r for r in self._relationships.values() if r.source_id == entity_id or r.target_id == entity_id)

    def remove(self, relationship_id: str) -> bool:
        return self._relationships.pop(relationship_id, None) is not None

    def validate(self, available_entities: set[str]) -> GraphValidationResult:
        errors: list[str] = []
        for rid, rel in self._relationships.items():
            if rel.source_id == rel.target_id:
                errors.append(f"Relationship '{rid}' is self-referencing")
            if rel.source_id not in available_entities:
                errors.append(f"Relationship '{rid}' source '{rel.source_id}' not found")
            if rel.target_id not in available_entities:
                errors.append(f"Relationship '{rid}' target '{rel.target_id}' not found")
            if not rel.relationship_type:
                errors.append(f"Relationship '{rid}' has no type")
        return GraphValidationResult(valid=len(errors) == 0, errors=tuple(errors))

    @property
    def count(self) -> int:
        return len(self._relationships)
