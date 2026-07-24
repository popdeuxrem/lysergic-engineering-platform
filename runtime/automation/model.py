from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class TriggerDefinition:
    trigger_id: str
    trigger_type: str  # event, schedule, manual
    source: str = ""
    config: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AutomationAction:
    action_id: str
    target: str  # workflow, ai, plugin
    target_id: str = ""
    input: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionPolicy:
    policy_id: str = "default"
    allowed_targets: tuple[str, ...] = ("workflow", "ai", "plugin")
    require_approval: bool = False
    max_executions: int = 0
    allowed_environments: tuple[str, ...] = ()


@dataclass(frozen=True)
class AutomationMetadata:
    automation_id: str
    name: str
    version: str = "0.1.0"
    description: str = ""
    owner: str = ""
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None


@dataclass
class AutomationExecution:
    execution_id: str
    automation_id: str
    trigger_type: str = ""
    status: str = "pending"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: str = ""
    error: str = ""


@dataclass
class Automation:
    automation_id: str
    name: str
    version: str = "0.1.0"
    description: str = ""
    triggers: tuple[TriggerDefinition, ...] = ()
    actions: tuple[AutomationAction, ...] = ()
    policy: ExecutionPolicy = field(default_factory=ExecutionPolicy)
    owner: str = ""
    tags: tuple[str, ...] = ()
    config: dict[str, Any] = field(default_factory=dict)
