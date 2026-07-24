from __future__ import annotations

from typing import Any

from runtime.services.events import EventBus
from runtime.services.registry import ServiceStatus
from runtime.workflows.dependency import WorkflowDependencyValidator
from runtime.workflows.events import WorkflowEventPublisher
from runtime.workflows.executor import WorkflowExecutor
from runtime.workflows.history import WorkflowHistory
from runtime.workflows.lifecycle import WorkflowLifecycle, WorkflowStatus
from runtime.workflows.model import WorkflowDefinition, WorkflowResult
from runtime.workflows.registry import WorkflowRegistry
from runtime.workflows.snapshot import WorkflowSnapshot
from runtime.workflows.validator import WorkflowValidator


class WorkflowManager:
    service_id = "workflow.manager"
    dependencies: tuple[str, ...] = ()

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._registry = WorkflowRegistry()
        self._lifecycle = WorkflowLifecycle()
        self._executor = WorkflowExecutor(self._lifecycle)
        self._validator = WorkflowValidator()
        self._history = WorkflowHistory()
        self._events = WorkflowEventPublisher(event_bus)
        self._dependency = WorkflowDependencyValidator()
        self._snapshot_version = 0
        self._snapshot: WorkflowSnapshot | None = None
        self._initialized = False

    @property
    def registry(self) -> WorkflowRegistry:
        return self._registry

    @property
    def lifecycle(self) -> WorkflowLifecycle:
        return self._lifecycle

    @property
    def executor(self) -> WorkflowExecutor:
        return self._executor

    @property
    def validator(self) -> WorkflowValidator:
        return self._validator

    @property
    def history(self) -> WorkflowHistory:
        return self._history

    @property
    def dependency(self) -> WorkflowDependencyValidator:
        return self._dependency

    @property
    def snapshot(self) -> WorkflowSnapshot | None:
        return self._snapshot

    @property
    def manager_status(self) -> ServiceStatus:
        return ServiceStatus.READY if self._initialized else ServiceStatus.PENDING

    def initialize(self) -> None:
        if self._initialized:
            return
        self._registry = WorkflowRegistry()
        self._lifecycle = WorkflowLifecycle()
        self._executor = WorkflowExecutor(self._lifecycle)
        self._validator = WorkflowValidator()
        self._history = WorkflowHistory()
        self._events = WorkflowEventPublisher(self._events._event_bus)
        self._dependency = WorkflowDependencyValidator()
        self._snapshot_version = 0
        self._initialized = True
        self._freeze_snapshot()

    def shutdown(self) -> None:
        self._registry = WorkflowRegistry()
        self._snapshot = None
        self._initialized = False

    def create(self, definition: WorkflowDefinition) -> WorkflowDefinition:
        self._registry.register(definition)
        self._lifecycle.initialize(definition.workflow_id)
        self._events.created(definition.workflow_id)
        self._freeze_snapshot()
        return definition

    def get(self, workflow_id: str) -> WorkflowDefinition | None:
        return self._registry.get(workflow_id)

    def list(self) -> tuple[WorkflowDefinition, ...]:
        return self._registry.list()

    def register(self, definition: WorkflowDefinition) -> WorkflowDefinition:
        return self.create(definition)

    def validate(self, workflow_id: str) -> WorkflowDefinition | None:
        definition = self._registry.get(workflow_id)
        if definition is None:
            return None
        result = self._validator.validate_tier1(definition)
        if result.valid:
            result2 = self._validator.validate_tier2(definition)
            if result2.valid:
                self._lifecycle.transition(workflow_id, WorkflowStatus.VALIDATED)
                self._events.validated(workflow_id)
            else:
                self._lifecycle.transition(workflow_id, WorkflowStatus.FAILED)
                self._events.failed(workflow_id, "; ".join(result2.errors))
        else:
            self._lifecycle.transition(workflow_id, WorkflowStatus.FAILED)
            self._events.failed(workflow_id, "; ".join(result.errors))
        self._freeze_snapshot()
        return definition

    def execute(self, workflow_id: str) -> WorkflowResult | None:
        definition = self._registry.get(workflow_id)
        if definition is None:
            return None
        if self._lifecycle.state_of(workflow_id) == WorkflowStatus.CREATED:
            self._lifecycle.transition(workflow_id, WorkflowStatus.VALIDATED)
        if self._lifecycle.state_of(workflow_id) == WorkflowStatus.VALIDATED:
            self._lifecycle.transition(workflow_id, WorkflowStatus.READY)
        if not self._lifecycle.can_transition(workflow_id, WorkflowStatus.RUNNING):
            return None
        self._events.started(workflow_id)
        result = self._executor.execute(definition)
        if result.status == "completed":
            self._events.completed(workflow_id)
        elif result.status == "failed":
            self._events.failed(workflow_id, result.error)
        elif result.status == "stopped":
            self._events.stopped(workflow_id)
        self._history.record(result)
        self._freeze_snapshot()
        return result

    def stop(self, workflow_id: str) -> WorkflowResult | None:
        result = self._executor.stop(workflow_id)
        if result is not None:
            self._history.record(result)
            self._events.stopped(workflow_id)
        self._freeze_snapshot()
        return result

    def status(self, workflow_id: str) -> str | None:
        state = self._lifecycle.state_of(workflow_id)
        return state.value if state else None

    def get_history(self, workflow_id: str) -> tuple[Any, ...]:
        return self._history.get(workflow_id)

    def snapshot_state(self) -> WorkflowSnapshot:
        return WorkflowSnapshot(definitions=self._registry.list(), version=self._snapshot_version)

    def _freeze_snapshot(self) -> None:
        self._snapshot_version += 1
        self._snapshot = WorkflowSnapshot(definitions=self._registry.list(), version=self._snapshot_version)
