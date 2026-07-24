from __future__ import annotations

from extensions.ecp.graph import ECPEntity, GraphValidationResult


class EntityRegistry:
    def __init__(self) -> None:
        self._entities: dict[str, ECPEntity] = {}

    def create(self, entity: ECPEntity) -> ECPEntity:
        if entity.entity_id in self._entities:
            raise ValueError(f"Entity already exists: {entity.entity_id}")
        self._entities[entity.entity_id] = entity
        return entity

    def get(self, entity_id: str) -> ECPEntity | None:
        return self._entities.get(entity_id)

    def list(self) -> tuple[ECPEntity, ...]:
        return tuple(self._entities.values())

    def list_by_type(self, entity_type: str) -> tuple[ECPEntity, ...]:
        return tuple(e for e in self._entities.values() if e.entity_type == entity_type)

    def remove(self, entity_id: str) -> bool:
        return self._entities.pop(entity_id, None) is not None

    def validate(self) -> GraphValidationResult:
        errors: list[str] = []
        seen = set()
        for eid, entity in self._entities.items():
            if eid in seen:
                errors.append(f"Duplicate entity ID: {eid}")
            seen.add(eid)
            if not entity.entity_type:
                errors.append(f"Entity '{eid}' has no type")
        return GraphValidationResult(valid=len(errors) == 0, errors=tuple(errors))

    @property
    def count(self) -> int:
        return len(self._entities)
