from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime.ai.evaluator import Evaluator
from runtime.ai.events import AIEventPublisher
from runtime.ai.executor import AIExecutor
from runtime.ai.lifecycle import AgentLifecycle, AgentLifecycleState
from runtime.ai.memory import AgentMemory
from runtime.ai.model import Agent, AgentExecution, AgentMetadata
from runtime.ai.permissions import AgentPermissions
from runtime.ai.planner import Planner
from runtime.ai.registry import AgentRegistry
from runtime.ai.snapshot import AISnapshot
from runtime.ai.telemetry import Telemetry
from runtime.ai.tools import ToolInvocation
from runtime.ai.validator import AIValidator
from runtime.services.events import EventBus
from runtime.services.registry import ServiceStatus


class AIManager:
    service_id = "ai.manager"
    dependencies: tuple[str, ...] = ()

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._registry = AgentRegistry()
        self._lifecycle = AgentLifecycle()
        self._executor = AIExecutor()
        self._planner = Planner()
        self._memory = AgentMemory()
        self._tools = ToolInvocation()
        self._permissions = AgentPermissions()
        self._evaluator = Evaluator()
        self._validator = AIValidator()
        self._telemetry = Telemetry()
        self._events = AIEventPublisher(event_bus)
        self._snapshot_version = 0
        self._snapshot: AISnapshot | None = None
        self._initialized = False

    @property
    def registry(self) -> AgentRegistry:
        return self._registry

    @property
    def lifecycle(self) -> AgentLifecycle:
        return self._lifecycle

    @property
    def executor(self) -> AIExecutor:
        return self._executor

    @property
    def planner(self) -> Planner:
        return self._planner

    @property
    def memory(self) -> AgentMemory:
        return self._memory

    @property
    def tools(self) -> ToolInvocation:
        return self._tools

    @property
    def permissions(self) -> AgentPermissions:
        return self._permissions

    @property
    def evaluator(self) -> Evaluator:
        return self._evaluator

    @property
    def telemetry(self) -> Telemetry:
        return self._telemetry

    @property
    def snapshot(self) -> AISnapshot | None:
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
        self._registry = AgentRegistry()
        self._snapshot = None
        self._initialized = False

    def create_agent(self, agent_id: str, name: str, **kwargs: Any) -> Agent:
        meta = AgentMetadata(agent_id=agent_id, name=name, **{k: v for k, v in kwargs.items() if k in ("version", "model", "description", "owner", "tags")})
        agent = Agent(agent_id=agent_id, name=name, version=kwargs.get("version", "0.1.0"), metadata=meta, model=kwargs.get("model", ""), description=kwargs.get("description", ""), owner=kwargs.get("owner", ""), tags=kwargs.get("tags", ()))
        self._registry.register(agent)
        self._lifecycle.initialize(agent_id)
        self._events.created(agent_id)
        self._freeze_snapshot()
        return agent

    def get_agent(self, agent_id: str) -> Agent | None:
        return self._registry.get(agent_id)

    def list_agents(self) -> tuple[Agent, ...]:
        return self._registry.list()

    def register_agent(self, agent_id: str) -> Agent | None:
        agent = self._registry.get(agent_id)
        if agent is None:
            return None
        self._lifecycle.transition(agent_id, AgentLifecycleState.REGISTERED)
        self._events.registered(agent_id)
        self._freeze_snapshot()
        return agent

    def validate_agent(self, agent_id: str) -> Agent | None:
        agent = self._registry.get(agent_id)
        if agent is None:
            return None
        vr = self._validator.validate_tier1(agent)
        if vr.valid:
            vr2 = self._validator.validate_tier2(agent, set())
            if vr2.valid:
                self._lifecycle.transition(agent_id, AgentLifecycleState.VALIDATED)
                self._events.validated(agent_id)
            else:
                self._lifecycle.transition(agent_id, AgentLifecycleState.FAILED)
                self._events.failed(agent_id, "; ".join(vr2.errors))
        else:
            self._lifecycle.transition(agent_id, AgentLifecycleState.FAILED)
            self._events.failed(agent_id, "; ".join(vr.errors))
        self._freeze_snapshot()
        return agent

    def ready_agent(self, agent_id: str) -> Agent | None:
        agent = self._registry.get(agent_id)
        if agent is None:
            return None
        self._lifecycle.transition(agent_id, AgentLifecycleState.READY)
        self._freeze_snapshot()
        return agent

    def execute(self, agent_id: str, prompt: str, session_id: str = "", context: dict[str, Any] | None = None) -> AgentExecution:
        agent = self._registry.get(agent_id)
        exec_id = f"{agent_id}-exec-{self._telemetry.total_executions + 1}"
        execution = AgentExecution(execution_id=exec_id, agent_id=agent_id, status="running", started_at=datetime.now(UTC), input_data=prompt)

        if agent is None:
            execution.status = "failed"
            execution.error = "Agent not found"
            return execution

        self._lifecycle.transition(agent_id, AgentLifecycleState.RUNNING)
        self._events.started(agent_id)
        self._events.execution_started(agent_id, exec_id)

        if session_id:
            self._memory.create_session(session_id)
            self._memory.set(session_id, "last_prompt", prompt)

        start = datetime.now(UTC)
        try:
            output = self._executor.execute(prompt, context)
            execution.output = output
            execution.status = "completed"
            execution.duration_ms = (datetime.now(UTC) - start).total_seconds() * 1000
            self._telemetry.record(agent_id, "execution", execution.duration_ms, success=True)
            self._events.execution_completed(agent_id, exec_id)
            self._evaluator.evaluate(exec_id, agent_id, output)
        except Exception as e:  # noqa: BLE001
            execution.status = "failed"
            execution.error = str(e)
            execution.duration_ms = (datetime.now(UTC) - start).total_seconds() * 1000
            self._telemetry.record(agent_id, "execution", execution.duration_ms, success=False, error=str(e))
            self._lifecycle.transition(agent_id, AgentLifecycleState.FAILED)
            self._events.failed(agent_id, str(e))

        execution.completed_at = datetime.now(UTC)
        self._freeze_snapshot()
        return execution

    def stop_agent(self, agent_id: str) -> Agent | None:
        agent = self._registry.get(agent_id)
        if agent is None:
            return None
        self._lifecycle.transition(agent_id, AgentLifecycleState.STOPPED)
        self._events.stopped(agent_id)
        self._freeze_snapshot()
        return agent

    def archive_agent(self, agent_id: str) -> Agent | None:
        agent = self._registry.get(agent_id)
        if agent is None:
            return None
        self._lifecycle.transition(agent_id, AgentLifecycleState.ARCHIVED)
        self._freeze_snapshot()
        return agent

    def status(self, agent_id: str) -> str | None:
        state = self._lifecycle.state_of(agent_id)
        return state.value if state else None

    def evaluate(self, execution_id: str, agent_id: str, output: Any = None) -> dict[str, Any]:
        result = self._evaluator.evaluate(execution_id, agent_id, output)
        return {"execution_id": result.execution_id, "valid": result.valid, "score": result.score, "metrics": result.metrics}

    def snapshot_state(self) -> AISnapshot:
        agents = {a.agent_id: a for a in self._registry.list()}
        return AISnapshot(agents=agents, version=self._snapshot_version)

    def _freeze_snapshot(self) -> None:
        self._snapshot_version += 1
        agents = {a.agent_id: a for a in self._registry.list()}
        self._snapshot = AISnapshot(agents=agents, version=self._snapshot_version)
