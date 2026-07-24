from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class KnowledgeSource:
    source_id: str
    source_type: str
    name: str
    reference: str = ""


@dataclass(frozen=True)
class KnowledgeReference:
    ref_id: str
    ref_type: str
    description: str = ""


@dataclass(frozen=True)
class KnowledgeMetadata:
    knowledge_id: str
    title: str
    kind: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None


@dataclass
class KnowledgeItem:
    knowledge_id: str
    title: str
    kind: str
    content: str = ""
    version: str = "0.1.0"
    metadata: KnowledgeMetadata | None = None
    source: KnowledgeSource | None = None
    references: tuple[KnowledgeReference, ...] = ()
    tags: tuple[str, ...] = ()
    description: str = ""
    author: str = ""
