from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class ExtensionLifecycleState(Enum):
    DISCOVERED = "discovered"
    VALIDATED = "validated"
    LOADING = "loading"
    READY = "ready"
    FAILED = "failed"
    STOPPING = "stopping"
    STOPPED = "stopped"
    REMOVED = "removed"


@dataclass
class LifecycleRecord:
    state: ExtensionLifecycleState = ExtensionLifecycleState.DISCOVERED
    transitions: dict[str, datetime] = field(default_factory=dict)
    error: str = ""

    def transition_to(self, target: ExtensionLifecycleState, error: str = "") -> None:
        allowed: dict[ExtensionLifecycleState, tuple[ExtensionLifecycleState, ...]] = {
            ExtensionLifecycleState.DISCOVERED: (ExtensionLifecycleState.VALIDATED, ExtensionLifecycleState.FAILED, ExtensionLifecycleState.REMOVED),
            ExtensionLifecycleState.VALIDATED: (ExtensionLifecycleState.LOADING, ExtensionLifecycleState.FAILED, ExtensionLifecycleState.REMOVED),
            ExtensionLifecycleState.LOADING: (ExtensionLifecycleState.READY, ExtensionLifecycleState.FAILED),
            ExtensionLifecycleState.READY: (ExtensionLifecycleState.STOPPING, ExtensionLifecycleState.STOPPED, ExtensionLifecycleState.FAILED),
            ExtensionLifecycleState.FAILED: (ExtensionLifecycleState.REMOVED,),
            ExtensionLifecycleState.STOPPING: (ExtensionLifecycleState.STOPPED, ExtensionLifecycleState.FAILED),
            ExtensionLifecycleState.STOPPED: (ExtensionLifecycleState.REMOVED, ExtensionLifecycleState.DISCOVERED),
            ExtensionLifecycleState.REMOVED: (),
        }
        valid = allowed.get(self.state, ())
        if target not in valid:
            raise ValueError(f"Cannot transition from {self.state.value} to {target.value}")
        self.state = target
        self.transitions[target.value] = datetime.now(UTC)
        if error:
            self.error = error


class ExtensionLifecycle:
    def __init__(self) -> None:
        self._records: dict[str, LifecycleRecord] = {}

    def register(self, extension_id: str) -> LifecycleRecord:
        record = LifecycleRecord()
        self._records[extension_id] = record
        return record

    def get(self, extension_id: str) -> LifecycleRecord | None:
        return self._records.get(extension_id)

    def transition(self, extension_id: str, target: ExtensionLifecycleState, error: str = "") -> None:
        record = self._records.get(extension_id)
        if record is None:
            raise KeyError(f"Extension '{extension_id}' not found in lifecycle")
        record.transition_to(target, error)

    def state_of(self, extension_id: str) -> ExtensionLifecycleState | None:
        record = self._records.get(extension_id)
        return record.state if record else None

    @property
    def records(self) -> dict[str, LifecycleRecord]:
        return dict(self._records)
