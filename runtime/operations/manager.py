from __future__ import annotations

from typing import Any

from runtime.operations.artifacts import ArtifactCollector
from runtime.operations.events import OperationsEventPublisher
from runtime.operations.executor import OperationsExecutor
from runtime.operations.gates import GateEngine
from runtime.operations.history import OperationsHistory
from runtime.operations.lifecycle import OperationLifecycle, OperationLifecycleState
from runtime.operations.model import (
    EngineeringOperation,
    OperationExecution,
)
from runtime.operations.planner import OperationPlanner
from runtime.operations.registry import OperationsRegistry
from runtime.operations.reports import OperationsReport
from runtime.operations.snapshot import OperationsSnapshot
from runtime.operations.validator import OperationsValidator
from runtime.services.events import EventBus
from runtime.services.registry import ServiceStatus


class OperationsManager:
    service_id = "operations.manager"
    dependencies: tuple[str, ...] = ()

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._registry = OperationsRegistry()
        self._lifecycle = OperationLifecycle()
        self._executor = OperationsExecutor()
        self._planner = OperationPlanner()
        self._validator = OperationsValidator()
        self._gates = GateEngine()
        self._artifacts = ArtifactCollector()
        self._reports = OperationsReport()
        self._history = OperationsHistory()
        self._events = OperationsEventPublisher(event_bus)
        self._snapshot_version = 0
        self._snapshot: OperationsSnapshot | None = None
        self._initialized = False

    @property
    def registry(self) -> OperationsRegistry:
        return self._registry

    @property
    def lifecycle(self) -> OperationLifecycle:
        return self._lifecycle

    @property
    def planner(self) -> OperationPlanner:
        return self._planner

    @property
    def gates(self) -> GateEngine:
        return self._gates

    @property
    def artifacts(self) -> ArtifactCollector:
        return self._artifacts

    @property
    def snapshot(self) -> OperationsSnapshot | None:
        return self._snapshot

    @property
    def manager_status(self) -> ServiceStatus:
        return ServiceStatus.READY if self._initialized else ServiceStatus.PENDING

    def initialize_runtime(self) -> None:
        if self._initialized:
            return
        self._snapshot_version = 0
        self._initialized = True
        self._freeze_snapshot()

    def shutdown(self) -> None:
        self._registry = OperationsRegistry()
        self._snapshot = None
        self._initialized = False

    def create(self, op_id: str, name: str, **kwargs: Any) -> EngineeringOperation:
        steps = kwargs.get("steps", ())
        gates = kwargs.get("gates", ())
        op = EngineeringOperation(operation_id=op_id, name=name, version=kwargs.get("version", "0.1.0"), description=kwargs.get("description", ""), steps=steps, gates=gates, owner=kwargs.get("owner", ""), tags=kwargs.get("tags", ()))
        self._registry.register(op)
        self._lifecycle.initialize(op_id)
        self._events.created(op_id)
        self._freeze_snapshot()
        return op

    def get(self, op_id: str) -> EngineeringOperation | None:
        return self._registry.get(op_id)

    def list(self) -> tuple[EngineeringOperation, ...]:
        return self._registry.list()

    def define(self, op_id: str) -> EngineeringOperation | None:
        op = self._registry.get(op_id)
        if op is None:
            return None
        self._lifecycle.transition(op_id, OperationLifecycleState.DEFINED)
        self._freeze_snapshot()
        return op

    def validate_op(self, op_id: str) -> EngineeringOperation | None:
        op = self._registry.get(op_id)
        if op is None:
            return None
        vr = self._validator.validate_tier1(op)
        if vr.valid:
            vr2 = self._validator.validate_tier2(op)
            if vr2.valid:
                self._lifecycle.transition(op_id, OperationLifecycleState.VALIDATED)
                self._events.validated(op_id)
            else:
                self._lifecycle.transition(op_id, OperationLifecycleState.FAILED)
                self._events.failed(op_id, "; ".join(vr2.errors))
        else:
            self._lifecycle.transition(op_id, OperationLifecycleState.FAILED)
            self._events.failed(op_id, "; ".join(vr.errors))
        self._freeze_snapshot()
        return op

    def prepare(self, op_id: str) -> EngineeringOperation | None:
        op = self._registry.get(op_id)
        if op is None:
            return None
        self._lifecycle.transition(op_id, OperationLifecycleState.READY)
        self._events.prepared(op_id)
        self._freeze_snapshot()
        return op

    def execute(self, op_id: str) -> OperationExecution | None:
        op = self._registry.get(op_id)
        if op is None:
            return None
        self._lifecycle.transition(op_id, OperationLifecycleState.EXECUTING)
        self._events.started(op_id)
        gate_results = self._gates.evaluate_all(op.gates)
        required_failed = [g for g, r in zip(op.gates, gate_results) if g.required and r.outcome == "fail"]
        if required_failed:
            for gate in required_failed:
                self._events.gate_failed(op_id, gate.gate_id)
            self._lifecycle.transition(op_id, OperationLifecycleState.FAILED)
            self._events.failed(op_id, f"Required gates failed: {[g.gate_id for g in required_failed]}")
            execution = OperationExecution(execution_id=f"{op_id}-exec-fail", operation_id=op_id, status="failed", error="Required gates failed")
            self._history.record(op.version, execution)
            self._freeze_snapshot()
            return execution
        for gate, result in zip(op.gates, gate_results):
            if result.outcome == "pass":
                self._events.gate_passed(op_id, gate.gate_id)
        execution = self._executor.execute(op)
        if execution.status == "completed":
            self._lifecycle.transition(op_id, OperationLifecycleState.COMPLETED)
            self._events.completed(op_id)
        else:
            self._lifecycle.transition(op_id, OperationLifecycleState.FAILED)
            self._events.failed(op_id, execution.error)
        self._history.record(op.version, execution)
        self._freeze_snapshot()
        return execution

    def status(self, op_id: str) -> str | None:
        state = self._lifecycle.state_of(op_id)
        return state.value if state else None

    def report(self, op_id: str, execution_id: str) -> dict[str, Any] | None:
        return self._reports.get(execution_id)

    def history(self, op_id: str) -> tuple[Any, ...]:
        return self._history.get(op_id)

    def archive(self, op_id: str) -> EngineeringOperation | None:
        op = self._registry.get(op_id)
        if op is None:
            return None
        self._lifecycle.transition(op_id, OperationLifecycleState.ARCHIVED)
        self._freeze_snapshot()
        return op

    def snapshot_state(self) -> OperationsSnapshot:
        ops = {o.operation_id: o for o in self._registry.list()}
        return OperationsSnapshot(operations=ops, version=self._snapshot_version)

    def _freeze_snapshot(self) -> None:
        self._snapshot_version += 1
        ops = {o.operation_id: o for o in self._registry.list()}
        self._snapshot = OperationsSnapshot(operations=ops, version=self._snapshot_version)
