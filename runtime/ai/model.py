from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class AgentCapability:
    capability_id: str
    version: str = "1.0.0"
    description: str = ""


@dataclass(frozen=True)
class AgentContext:
    session_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentMetadata:
    agent_id: str
    name: str
    version: str = "0.1.0"
    model: str = ""
    description: str = ""
    owner: str = ""
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class AgentExecution:
    execution_id: str
    agent_id: str
    status: str = "pending"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    input_data: Any = None
    output: Any = None
    error: str = ""
    duration_ms: float = 0.0


@dataclass
class Agent:
    agent_id: str
    name: str
    version: str = "0.1.0"
    metadata: AgentMetadata | None = None
    capabilities: tuple[AgentCapability, ...] = ()
    description: str = ""
    model: str = ""
    owner: str = ""
    tags: tuple[str, ...] = ()
    config: dict[str, Any] = field(default_factory=dict)
