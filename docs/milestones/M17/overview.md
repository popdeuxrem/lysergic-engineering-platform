# M17 — Extension Runtime Architecture

**Milestone:** LEP-M17
**Objective:** Define the extension system contract for LEP capabilities
**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)
**Runtime Freeze:** M15 — Complete
**Kilo CLI:** M16 — Complete
**Status:** Design Phase

---

## 1. M17 Objective

Design the Extension Runtime that manages LEP extensions through their
complete lifecycle: discovery, validation, installation, loading,
initialization, execution, and removal.

The Extension Runtime is the bridge between Kilo CLI (and other consumers)
and the Extension SDK that extensions use internally.

---

## 2. Extension Runtime Purpose

The Extension Runtime manages extension lifecycle. It does not implement
extension capabilities — that is the responsibility of individual extensions.

| Concern | Owner |
|---------|-------|
| Extension discovery | Extension Runtime |
| Manifest validation | Extension Runtime |
| Lifecycle orchestration | Extension Runtime |
| Permission enforcement | Extension Runtime |
| Capability registration | Extension Runtime |
| Domain capability | Individual extension |
| Implementation logic | Individual extension |
| Extension-specific contracts | Individual extension |

---

## 3. Relationship to LEP Architecture

```
Kilo CLI  (M16)
    │
    ▼
Extension Runtime  (M17 — this milestone)
    │
    ├── Extension SDK  (LID-0004, already implemented)
    │       │
    │       ▼
    │   Extension implementations
    │
    ▼
Runtime Public API  (runtime.api.*)
    │
    ▼
Platform Services / Runtime Kernel  (M15 frozen)
```

### Layer Rules

- Extension Runtime imports from `runtime.api.*` (same as Kilo CLI)
- Extension Runtime imports from `extensions.sdk.*` (the SDK)
- Extensions import from `extensions.sdk.*` (not runtime directly)
- Kilo CLI imports the Extension Runtime adapter (not the SDK directly)
- No layer may import from `runtime.kernel.*` or `runtime.services.*`

---

## 4. Why Capabilities Belong in Extensions

| Reason | Detail |
|--------|--------|
| Isolation | Extensions are independently deployable, testable, and versioned |
| Stability | The runtime freezes; extensions evolve |
| Ownership | Domain teams own their extensions |
| Security | Permission model scopes extension access |
| Scale | New capabilities don't require runtime changes |

---

## 5. Scope

### In Scope (M17)

| Item | Description |
|------|-------------|
| Extension contract | Manifest schema, lifecycle, permission model |
| Extension Runtime design | Registry, lifecycle, validation, discovery |
| CLI interface | Kilo commands for extension management |
| Extension SDK integration | Runtime consumes `extensions.sdk.*` |
| Validation strategy | Tier 1 and Tier 2 validation |
| Release criteria | `extension-runtime-v0.1.0` |

### Not in Scope (M17)

| Item | Reason |
|------|--------|
| ECP Runtime | Separate milestone |
| AI Runtime extensions | Already exists as `runtime/ai/` |
| MCP Integration | Future milestone |
| Extension implementation | Extensions implement their own logic |
| Plugin system | Already exists as `runtime/plugins/` |
| Extension marketplace | Future concern |

### Downstream Consumers (Post-M17)

Once the Extension Runtime is operational, it will be consumed by:

| Consumer | Relationship |
|----------|--------------|
| **ECP Runtime** | Engineering Control Plane runs as an extension |
| **AI Runtime** | AI capabilities may be exposed through extensions |
| **MCP Integration** | MCP tools are loaded as extensions |
| **Automation Runtime** | Automation actions can target extensions |

These consumers are NOT part of M17. They are downstream milestones.
