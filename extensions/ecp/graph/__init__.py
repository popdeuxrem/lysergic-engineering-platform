from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class ECPEntity:
    entity_id: str
    entity_type: str
    version: str = "0.1.0"
    name: str = ""
    description: str = ""
    owner: str = ""
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ECPRelationship:
    relationship_id: str
    relationship_type: str
    source_id: str
    target_id: str
    version: str = "0.1.0"
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ECPReference:
    reference_id: str
    ref_type: str
    target_type: str
    target_id: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
