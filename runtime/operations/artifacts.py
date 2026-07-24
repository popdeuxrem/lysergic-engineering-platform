from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class OperationArtifact:
    artifact_id: str
    name: str
    artifact_type: str
    source: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


class ArtifactCollector:
    def __init__(self) -> None:
        self._artifacts: dict[str, list[OperationArtifact]] = {}

    def collect(self, op_id: str, artifact: OperationArtifact) -> None:
        if op_id not in self._artifacts:
            self._artifacts[op_id] = []
        self._artifacts[op_id].append(artifact)

    def get(self, op_id: str) -> tuple[OperationArtifact, ...]:
        return tuple(self._artifacts.get(op_id, []))

    def remove(self, op_id: str) -> bool:
        return self._artifacts.pop(op_id, None) is not None
