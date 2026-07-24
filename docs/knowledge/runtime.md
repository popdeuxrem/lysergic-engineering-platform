# LEP Knowledge Runtime v1.0

## Overview

The LEP Knowledge Runtime provides governed management of engineering knowledge
artifacts with identity, ingestion, validation, provenance, cataloging, search,
lifecycle management, and controlled retrieval.

## Architecture

```
KnowledgeManager (orchestrator)
  ├── KnowledgeRegistry       — deterministic registration, kind/tag filtering
  ├── KnowledgeLifecycle      — 7-state machine (CREATED → ... → ARCHIVED)
  ├── KnowledgeCatalog        — indexing, filtering, metadata retrieval
  ├── KnowledgeSearch         — title/metadata/tag/keyword search (no AI/vectors)
  ├── KnowledgeResolver       — URN-based resolution (urn:lep:knowledge:{kind}:{id})
  ├── KnowledgeIngestion      — controlled ingestion from assets/projects/external
  ├── KnowledgeValidator      — Tier 1 (schema/metadata), Tier 2 (provenance/deps)
  ├── ProvenanceTracker       — origin, creator, transformations, relationships
  ├── KnowledgeEventPublisher — EventBus integration (7 events)
  └── KnowledgeSnapshot       — immutable state snapshots
```

## Lifecycle States

```
CREATED → INGESTED → VALIDATED → AVAILABLE → DEPRECATED → ARCHIVED
    │        │           │           │            │
    └─ FAILED ┴─ FAILED ──┴── FAILED ─┴── FAILED ─┴─ FAILED
FAILED → CREATED (retry)
ARCHIVED → AVAILABLE (restore)
```

## Knowledge Model

| Concept | Type | Description |
|---------|------|-------------|
| `KnowledgeItem` | dataclass | Identity, title, kind, content, version |
| `KnowledgeMetadata` | frozen dataclass | knowledge_id, title, kind, version, author, tags, timestamps |
| `KnowledgeSource` | frozen dataclass | source_id, source_type, name, reference |
| `KnowledgeReference` | frozen dataclass | ref_id, ref_type, description |

## Ingestion Sources

- **Direct**: created directly through the KnowledgeManager
- **Asset**: ingested from Asset Runtime artifacts
- **Project**: ingested from Project Runtime entities
- **External**: via the provider interface

## Provenance Tracking

Provenance records capture:
- Origin (how the knowledge was created)
- Source (source system/artifact reference)
- Creator (author/provider)
- Creation timestamp
- Transformations (validation, ingestion, etc.)
- Relationships (derived-from, references)

## Search (v1.0)

- Title search
- Description/keyword search
- Tag search
- Kind filtering

No embeddings, vector databases, or AI retrieval.

## Events

- `knowledge.KnowledgeCreated`
- `knowledge.KnowledgeIngested`
- `knowledge.KnowledgeValidated`
- `knowledge.KnowledgePublished`
- `knowledge.KnowledgeDeprecated`
- `knowledge.KnowledgeArchived`
- `knowledge.KnowledgeFailed`

## Validation Tiers

**Tier 1:** Schema validation, metadata validation (knowledge_id, title, kind required)
**Tier 2:** Provenance validation, source validity, duplicate reference detection

## Future Evolution

- Embedding-based semantic search
- Vector database integration
- AI-powered knowledge retrieval
- Knowledge graph construction
- Cross-runtime knowledge federation
