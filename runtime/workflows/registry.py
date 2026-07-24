from __future__ import annotations

from runtime.workflows.exceptions import RegistryFrozenError
from runtime.workflows.model import WorkflowDefinition


class WorkflowRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, WorkflowDefinition] = {}
        self._frozen = False

    def register(self, definition: WorkflowDefinition) -> None:
        if self._frozen:
            from runtime.workflows.exceptions import RegistryFrozenError
            raise RegistryFrozenError()
        if definition.workflow_id in self._definitions:
            from runtime.workflows.exceptions import WorkflowConflictError
            raise WorkflowConflictError(definition.workflow_id)
        self._definitions[definition.workflow_id] = definition

    def get(self, workflow_id: str) -> WorkflowDefinition | None:
        return self._definitions.get(workflow_id)

    def unregister(self, workflow_id: str) -> bool:
        if self._frozen:
            raise RegistryFrozenError()
        return self._definitions.pop(workflow_id, None) is not None

    def list(self) -> tuple[WorkflowDefinition, ...]:
        return tuple(self._definitions.values())

    def list_by_tag(self, tag: str) -> tuple[WorkflowDefinition, ...]:
        return tuple(w for w in self._definitions.values() if tag in w.tags)

    def freeze(self) -> None:
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def count(self) -> int:
        return len(self._definitions)

    def __contains__(self, workflow_id: str) -> bool:
        return workflow_id in self._definitions
