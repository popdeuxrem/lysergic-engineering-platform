from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.workflows.model import WorkflowDefinition


class WorkflowSnapshot:
    def __init__(self, definitions: dict[str, WorkflowDefinition] | tuple[WorkflowDefinition, ...], version: int = 0) -> None:
        if isinstance(definitions, tuple):
            self._definitions = {w.workflow_id: w for w in definitions}
        else:
            self._definitions = dict(definitions)
        self._version = version
        self._timestamp = datetime.now(UTC)

    def get(self, workflow_id: str) -> WorkflowDefinition | None:
        return self._definitions.get(workflow_id)

    def list(self) -> tuple[WorkflowDefinition, ...]:
        return tuple(self._definitions.values())

    def count(self) -> int:
        return len(self._definitions)

    @property
    def version(self) -> int:
        return self._version

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self._version,
            "timestamp": self._timestamp.isoformat(),
            "workflows": [{"workflow_id": w.workflow_id, "name": w.name, "version": w.version} for w in self._definitions.values()],
        }
