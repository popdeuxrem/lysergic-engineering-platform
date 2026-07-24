from __future__ import annotations

from extensions.ecp.graph import ECPReference, GraphValidationResult


class ReferenceResolver:
    def __init__(self) -> None:
        self._references: dict[str, ECPReference] = {}

    def register(self, reference: ECPReference) -> ECPReference:
        if reference.reference_id in self._references:
            raise ValueError(f"Reference already exists: {reference.reference_id}")
        self._references[reference.reference_id] = reference
        return reference

    def get(self, reference_id: str) -> ECPReference | None:
        return self._references.get(reference_id)

    def resolve(self, target_type: str, target_id: str) -> tuple[ECPReference, ...]:
        return tuple(r for r in self._references.values() if r.target_type == target_type and r.target_id == target_id)

    def remove(self, reference_id: str) -> bool:
        return self._references.pop(reference_id, None) is not None

    def validate(self, available_targets: set[tuple[str, str]]) -> GraphValidationResult:
        errors: list[str] = []
        for rid, ref in self._references.items():
            key = (ref.target_type, ref.target_id)
            if key not in available_targets:
                errors.append(f"Reference '{rid}' target '{ref.target_type}:{ref.target_id}' not found")
        return GraphValidationResult(valid=len(errors) == 0, errors=tuple(errors))

    @property
    def count(self) -> int:
        return len(self._references)
