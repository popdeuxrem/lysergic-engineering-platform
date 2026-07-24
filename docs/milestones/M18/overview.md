# M18 — ECP Runtime Integration Architecture

**Milestone:** LEP-M18
**Objective:** Define how the Engineering Control Plane integrates as a governed LEP extension
**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)
**Dependencies:** M15 (Runtime) ✅, M16 (Kilo CLI) ✅, M17 (Extension Runtime) ✅
**Status:** Design Phase

---

## 1. M18 Objective

Design the integration contract between the LEP Runtime Platform and the
Engineering Control Plane (ECP). ECP provides governance graph semantics —
entities, relationships, references, and graph validation — as a governed
LEP extension.

---

## 2. Purpose of ECP Runtime Integration

ECP is a domain-specific extension that implements the LEP governance model
as executable runtime capabilities. It is NOT the platform foundation.

| Capability | Owner |
|-----------|-------|
| Graph semantics | ECP |
| Entity management | ECP |
| Relationship management | ECP |
| Reference resolution | ECP |
| Graph validation | ECP |
| Runtime execution | LEP Runtime |
| Extension lifecycle | LEP Extension Runtime |
| Platform contracts | LEP |
| Validation framework | LEP |

---

## 3. Relationship Between LEP and ECP

```
LEP Runtime Platform
    │
    ├── Runtime Kernel (frozen M15)
    ├── Platform Services (frozen M15)
    ├── Core API (runtime.api.*)
    ├── Extension Runtime (M17)
    │       │
    │       ▼
    │   ECP Extension (M18 — this milestone)
    │       │
    │       ▼
    │   runtime.api.*
    │
    ├── Kilo CLI (M16)
    └── Other extensions
```

LEP provides the execution substrate. ECP provides the governance semantics.

### Constitutional Boundary

ECP enforces:
- **Constitutional Law 0:** Computation may produce judgments. Authority alone may produce decisions.
- **Dependency invariant:** Downward-only dependency graph.
- **Ownership invariant:** Every artifact has exactly one owner.
- **Specification invariant:** Programs consume specifications. Specifications never depend on programs.
- **Execution invariant:** Execution systems implement specifications but never redefine them.

These are ECP's responsibility. LEP provides the runtime for these rules
to execute within.

---

## 4. Why ECP Is Consumed as an Extension

| Reason | Detail |
|--------|--------|
| Isolation | ECP governance rules are independently versioned and deployed |
| Stability | The runtime freezes; ECP evolves |
| Security | Extension Runtime permission model scopes ECP access |
| Governance | ECP runs inside the same governance framework it defines |
| Evolution | New governance capabilities don't require runtime changes |

---

## 5. Scope

### In Scope (M18)

| Item | Description |
|------|-------------|
| ECP extension contract | Manifest, lifecycle, dependencies |
| ECP runtime adapter | Extension entry point, lifecycle hooks |
| Data boundaries | Storage, schema, validation ownership |
| Dependency rules | Allowed/forbidden import paths |
| Graph semantics integration | How ECP entities/relationships/references map |
| Release criteria | `ecp-runtime-v0.1.0-alpha` |

### Not in Scope (M18)

| Item | Reason |
|------|--------|
| ECP schema implementation | Separate implementation milestone |
| Graph database integration | Future concern |
| ECP-specific CLI commands | Future Kilo extension |
| Entity migration from existing artifacts | Separate process |
| ECP governance UI | Future concern |

### Downstream Consumers

Once the ECP Extension is operational, it will be consumed by:
- **Kilo CLI** — governance commands via `lep ecp` subcommands
- **Automation Runtime** — governance-aware automation actions
- **Engineering Operations** — operations with governance gate checks
- **AI Runtime** — AI-assisted governance recommendations (future)

---

## 6. Non-Scope Exclusions

| Item | Rationale |
|------|-----------|
| LEP constitutional redesign | LEP-ARCH-v0.1.0 is frozen |
| Graph schema redesign | ECP E0.x schemas are accepted |
| Entity/relationship redefinition | ECP metamodel is stable |
| Runtime kernel modification | M15 freeze is complete |
| Kilo CLI modification | M16 alpha is complete |
