from __future__ import annotations

from typing import Any

from runtime.automation.events import AutomationEventPublisher
from runtime.automation.executor import AutomationExecutor
from runtime.automation.history import AutomationHistory
from runtime.automation.lifecycle import AutomationLifecycle, AutomationLifecycleState
from runtime.automation.model import (
    Automation,
    AutomationExecution,
    ExecutionPolicy,
)
from runtime.automation.policies import PolicyEngine
from runtime.automation.registry import AutomationRegistry
from runtime.automation.scheduler import Scheduler
from runtime.automation.snapshot import AutomationSnapshot
from runtime.automation.triggers import TriggerRegistry
from runtime.automation.validator import AutomationValidator
from runtime.services.events import EventBus
from runtime.services.registry import ServiceStatus


class AutomationManager:
    service_id = "automation.manager"
    dependencies: tuple[str, ...] = ()

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._registry = AutomationRegistry()
        self._lifecycle = AutomationLifecycle()
        self._triggers = TriggerRegistry()
        self._scheduler = Scheduler()
        self._executor = AutomationExecutor()
        self._policies = PolicyEngine()
        self._validator = AutomationValidator()
        self._history = AutomationHistory()
        self._events = AutomationEventPublisher(event_bus)
        self._snapshot_version = 0
        self._snapshot: AutomationSnapshot | None = None
        self._initialized = False

    @property
    def registry(self) -> AutomationRegistry:
        return self._registry

    @property
    def lifecycle(self) -> AutomationLifecycle:
        return self._lifecycle

    @property
    def scheduler(self) -> Scheduler:
        return self._scheduler

    @property
    def policies(self) -> PolicyEngine:
        return self._policies

    @property
    def snapshot(self) -> AutomationSnapshot | None:
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
        self._registry = AutomationRegistry()
        self._snapshot = None
        self._initialized = False

    def create(self, automation_id: str, name: str, **kwargs: Any) -> Automation:
        triggers = kwargs.get("triggers", ())
        actions = kwargs.get("actions", ())
        policy = kwargs.get("policy", ExecutionPolicy())
        automation = Automation(automation_id=automation_id, name=name, version=kwargs.get("version", "0.1.0"), description=kwargs.get("description", ""), triggers=triggers, actions=actions, policy=policy, owner=kwargs.get("owner", ""), tags=kwargs.get("tags", ()))
        self._registry.register(automation)
        self._lifecycle.initialize(automation_id)
        self._events.created(automation_id)
        self._freeze_snapshot()
        return automation

    def get(self, automation_id: str) -> Automation | None:
        return self._registry.get(automation_id)

    def list(self) -> tuple[Automation, ...]:
        return self._registry.list()

    def validate_automation(self, automation_id: str) -> Automation | None:
        automation = self._registry.get(automation_id)
        if automation is None:
            return None
        vr = self._validator.validate_tier1(automation)
        if vr.valid:
            vr2 = self._validator.validate_tier2(automation)
            if vr2.valid:
                self._lifecycle.transition(automation_id, AutomationLifecycleState.VALIDATED)
                self._events.validated(automation_id)
            else:
                self._lifecycle.transition(automation_id, AutomationLifecycleState.FAILED)
                self._events.failed(automation_id, "; ".join(vr2.errors))
        else:
            self._lifecycle.transition(automation_id, AutomationLifecycleState.FAILED)
            self._events.failed(automation_id, "; ".join(vr.errors))
        self._freeze_snapshot()
        return automation

    def ready_automation(self, automation_id: str) -> Automation | None:
        automation = self._registry.get(automation_id)
        if automation is None:
            return None
        self._lifecycle.transition(automation_id, AutomationLifecycleState.READY)
        self._freeze_snapshot()
        return automation

    def enable(self, automation_id: str) -> Automation | None:
        automation = self._registry.get(automation_id)
        if automation is None:
            return None
        self._policies.check_execution(automation)
        self._lifecycle.transition(automation_id, AutomationLifecycleState.ENABLED)
        self._events.enabled(automation_id)
        self._freeze_snapshot()
        return automation

    def disable(self, automation_id: str) -> Automation | None:
        automation = self._registry.get(automation_id)
        if automation is None:
            return None
        self._lifecycle.transition(automation_id, AutomationLifecycleState.DISABLED)
        self._events.disabled(automation_id)
        self._freeze_snapshot()
        return automation

    def execute(self, automation_id: str, trigger_type: str = "manual") -> AutomationExecution | None:
        automation = self._registry.get(automation_id)
        if automation is None:
            return None
        self._lifecycle.transition(automation_id, AutomationLifecycleState.EXECUTING)
        self._events.started(automation_id)
        self._events.triggered(automation_id, trigger_type)
        execution = self._executor.execute(automation, trigger_type)
        self._history.record(execution)
        if execution.status == "completed":
            self._lifecycle.transition(automation_id, AutomationLifecycleState.ENABLED)
            self._events.completed(automation_id)
        else:
            self._lifecycle.transition(automation_id, AutomationLifecycleState.FAILED)
            self._events.failed(automation_id, execution.error)
        self._freeze_snapshot()
        return execution

    def status(self, automation_id: str) -> str | None:
        state = self._lifecycle.state_of(automation_id)
        return state.value if state else None

    def history(self, automation_id: str) -> tuple[Any, ...]:
        return self._history.get(automation_id)

    def archive(self, automation_id: str) -> Automation | None:
        automation = self._registry.get(automation_id)
        if automation is None:
            return None
        self._lifecycle.transition(automation_id, AutomationLifecycleState.ARCHIVED)
        self._freeze_snapshot()
        return automation

    def snapshot_state(self) -> AutomationSnapshot:
        automations = {a.automation_id: a for a in self._registry.list()}
        return AutomationSnapshot(automations=automations, version=self._snapshot_version)

    def _freeze_snapshot(self) -> None:
        self._snapshot_version += 1
        automations = {a.automation_id: a for a in self._registry.list()}
        self._snapshot = AutomationSnapshot(automations=automations, version=self._snapshot_version)
