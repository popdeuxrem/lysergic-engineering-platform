from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class OperationStep:
    step_id: str
    name: str
    target: str = ""
    target_id: str = ""
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationGate:
    gate_id: str
    gate_type: str
    required: bool = True
    description: str = ""
    result: str = "pending"


@dataclass(frozen=True)
class OperationMetadata:
    operation_id: str
    name: str
    version: str = "0.1.0"
    description: str = ""
    owner: str = ""
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None


@dataclass
class OperationExecution:
    execution_id: str
    operation_id: str
    status: str = "pending"
    started_at: datetime | None = None
    completed_at: datetime | None = None
    step_results: tuple[dict[str, Any], ...] = ()
    error: str = ""


@dataclass
class EngineeringOperation:
    operation_id: str
    name: str
    version: str = "0.1.0"
    description: str = ""
    steps: tuple[OperationStep, ...] = ()
    gates: tuple[ValidationGate, ...] = ()
    owner: str = ""
    tags: tuple[str, ...] = ()
    config: dict[str, Any] = field(default_factory=dict)
