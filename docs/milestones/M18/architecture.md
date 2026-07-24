# M18 — ECP Runtime Integration Architecture

**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)
**ECP Baseline:** ECP-RP-v0.1.0 (Accepted governance artifacts)

---

## 1. ECP Position

```
Kilo CLI  (M16)
    │
    ▼
Extension Runtime  (M17)
    │
    ├── discover → validate → install → enable
    │
    ▼
ECP Extension  (M18 — this milestone)
    │
    ├── extensions/ecp/
    │       ├── extension.yaml       (ECP manifest)
    │       ├── adapter.py           (runtime entry point)
    │       ├── graph/               (graph semantics)
    │       │   ├── entities.py
    │       │   ├── relationships.py
    │       │   ├── references.py
    │       │   └── validator.py
    │       └── lifecycle.py         (lifecycle hooks)
    │
    ▼
runtime.api.*  (LEP public API)
    │
    ├── LEP facade
    ├── DiagnosticsAPI
    ├── ValidationAPI
    └── publish_event(), RuntimeStatus
    │
    ▼
Runtime Kernel  (M15 frozen)
```

---

## 2. ECP Ownership Boundary

### LEP Owns

| Concern | Description |
|---------|-------------|
| Runtime execution | Platform lifecycle, service management |
| Extension lifecycle | Install, discover, validate, load, initialize, shutdown, remove |
| Platform contracts | `contracts/` — interface definitions |
| Validation framework | `profiles/` — validation rules |
| Schema framework | `schemas/` — JSON Schema definitions |
| Event infrastructure | EventBus, event publishing |
| CLI infrastructure | Kilo command framework |
| Security model | Permission enforcement, runtime.api boundaries |

### ECP Owns

| Concern | Description |
|---------|-------------|
| Governance graph semantics | Entity, relationship, reference definitions |
| Entity management | CRUD operations for governed entities |
| Relationship management | Edge creation, validation, lifecycle |
| Reference resolution | URN-based lookup across governed objects |
| Graph validation | Acyclic dependency enforcement, semantic rules |
| Constitutional invariants | Law 0 enforcement, dependency/ownership/specification/execution invariants |
| Evidence management | Acceptance package generation |
| Decision recording | Governance decision artifacts |
| Judgment computation | READY_FOR_ACCEPTANCE evaluation |

---

## 3. ECP Model Preservation

ECP defines a three-layer metamodel that must be preserved within the extension:

```
L0 Structural Primitives
    │
    ├── Identity
    ├── Reference
    ├── Version
    └── MetadataFragment
    │
    ▼
L1 Relationships
    │
    ├── OwnershipBinding
    ├── DependencyBinding
    └── CapabilityBinding
    │
    ▼
L2 Entities
    │
    ├── Artifact
    ├── Capability
    ├── Scope
    └── AuthorityContract
    │
    ▼
Graph Semantics
    │
    ├── Nodes (L2 entities)
    ├── Edges (L1 relationships)
    └── Validation (acyclic, complete, consistent)
```

### Merge Prohibitions

| Concept | Must NOT merge into | Rationale |
|---------|---------------------|-----------|
| References | Relationships | References are typed links; relationships are governed edges |
| Relationships | Entities | Relationships are edge definitions; entities are graph nodes |
| Entities | References | Entities have lifecycle; references are immutable value objects |
| Graph validation | Entity CRUD | Validation is a separate concern from mutation |

---

## 4. ECP Extension Manifest

```yaml
# extensions/ecp/extension.yaml
extension_id: ecp
name: Engineering Control Plane
version: 0.1.0
owner: PortfolioAuthority
description: >
  The Engineering Control Plane provides governance graph semantics
  for the LEP platform, including entity management, relationship
  management, reference resolution, and graph validation.

runtime_compatibility: ">=0.1.0,<1.0.0"

capabilities:
  - ecp.graph.manage         # Entity/relationship CRUD
  - ecp.graph.validate       # Graph integrity validation
  - ecp.graph.resolve        # URN-based reference resolution
  - ecp.governance.evidence  # Acceptance package generation
  - ecp.governance.decision  # Governance decision recording

lifecycle_hooks:
  on_install: ecp.lifecycle.install
  on_enable: ecp.lifecycle.enable
  on_disable: ecp.lifecycle.disable
  on_remove: ecp.lifecycle.remove

dependencies:
  - runtime
```

---

## 5. ECP Runtime Adapter

### Extension Entry Point

```python
# extensions/ecp/adapter.py (design sketch — not implementation)

class ECPAdapter:
    extension_id = "ecp"

    def __init__(self, lep: LEP) -> None:
        self._lep = lep
        self._graph = GraphEngine()
        self._entities = EntityRegistry()
        self._relationships = RelationshipRegistry()
        self._validator = GraphValidator()

    def initialize(self) -> None:
        # Load accepted ECP governance artifacts
        # Initialize graph engine
        # Register entity types
        pass

    def shutdown(self) -> None:
        # Persist pending state
        # Shutdown graph engine
        pass
```

### Lifecycle Hooks

| Hook | Trigger | Action |
|------|---------|--------|
| `on_install` | Extension Runtime: install | Deploy ECP schemas and contracts |
| `on_enable` | Extension Runtime: enable | Initialize graph engine, load governance state |
| `on_disable` | Extension Runtime: disable | Persist state, shutdown graph engine |
| `on_remove` | Extension Runtime: remove | Clean up ECP artifacts |

### Runtime API Usage

The ECP adapter consumes only:

| API | Purpose |
|-----|---------|
| `runtime.api.LEP` | Platform identity, version, health |
| `runtime.api.DiagnosticsAPI` | Runtime status, telemetry |
| `runtime.api.ValidationAPI` | Schema validation for ECP artifacts |
| `runtime.api.publish_event()` | Publish governance events |
| `runtime.api.RuntimeStatus` | Status reporting |

### Event Integration

The ECP extension publishes governance events through `runtime.api.publish_event()`:

```
ecp.EntityCreated
ecp.EntityValidated
ecp.RelationshipCreated
ecp.RelationshipValidated
ecp.GraphValidated
ecp.GovernanceDecisionRecorded
ecp.EvidencePackageGenerated
```

---

## 6. Data Boundaries

### Storage Ownership

| Data | Owner | Location |
|------|-------|----------|
| Governance graph state | ECP | `extensions/ecp/` (in-memory with persistence hooks) |
| Governance artifacts (decisions, evidence, judgments) | ECP | `decisions/`, `evidence/`, `judgments/` |
| Runtime state | LEP | `runtime/` |
| Extension state | LEP Extension Runtime | `runtime/extensions/` |

### Schema Ownership

| Schema | Owner | Location |
|--------|-------|----------|
| ECP entity/relationship schemas | ECP | `extensions/ecp/schemas/` |
| Platform schemas | LEP | `schemas/` |
| Validation profiles | LEP | `profiles/` |
| Contracts | LEP | `contracts/` |

### Validation Ownership

| Validation | Owner | Mechanism |
|------------|-------|-----------|
| Graph integrity (acyclic, complete, consistent) | ECP | `GraphValidator` |
| Schema compliance | LEP | `ValidationAPI.validate_schema()` |
| Lifecycle correctness | LEP Extension Runtime | Lifecycle state machine |
| Dependency satisfaction | LEP Extension Runtime | Dependency resolver |

### Graph Lifecycle

```
Entity Created  →  Entity Validated  →  Entity Published  →  Entity Deprecated  →  Entity Archived
     │                  │                     │                     │
     └── Relationship ──┘                     └── Graph Revalidated ──┘
```

---

## 7. Dependency Rules

### Allowed

```
ECP Extension (extensions/ecp/)
    │
    ├── extensions.sdk.*      (Extension SDK — manifest, compatibility)
    ├── runtime.api.*          (Runtime Public API — LEP, ValidationAPI, publish_event)
    └── stdlib                 (Standard library)
```

### Forbidden

```
ECP Extension (extensions/ecp/)
    │
    ├── runtime.kernel.*       ✗ (Runtime internals)
    ├── runtime.services.*     ✗ (Service layer)
    ├── runtime/assets/*       ✗ (Direct subsystem access)
    ├── runtime/workflows/*    ✗ (Direct subsystem access)
    ├── runtime/ai/*           ✗ (Direct subsystem access)
    ├── runtime/automation/*   ✗ (Direct subsystem access)
    ├── runtime/operations/*   ✗ (Direct subsystem access)
    ├── cli/kilo/*             ✗ (CLI layer)
    ├── contracts/*            ✗ (Contracts are for runtime definition)
    ├── schemas/*              ✗ (Schemas are for validation — consume via API)
    └── profiles/*             ✗ (Profiles are for validation)
```

### Enforcement

Import boundary is enforced via AST-based scan (same mechanism as
`tests/cli/test_import_boundary.py`), extended to cover `extensions/ecp/`.
