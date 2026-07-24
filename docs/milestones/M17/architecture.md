# M17 — Extension Runtime Architecture

**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)

---

## 1. Extension Runtime Position

```
Kilo CLI (lep extension install, lep extension list, ...)
    │
    ▼
Extension Runtime Adapter  (cli/kilo/adapter/extension.py)
    │
    ▼
Extension Runtime Manager  (runtime/extensions/manager.py)
    │
    ├── Extension Registry     → identity, state, metadata
    ├── Extension Lifecycle    → 8-state machine
    ├── Extension Loader       → discovery, manifest parsing
    ├── Extension Validator    → Tier 1/Tier 2 validation
    ├── Capability Coordinator → capability registration, conflict detection
    └── Permission Manager     → grant/deny by default
    │
    ▼
Extension SDK  (extensions/sdk/)
    │
    ▼
Extensions  (extensions/<name>/)
    │
    ▼
Runtime Public API  (runtime.api.*)
```

---

## 2. Extension Ownership Boundary

### Extension Runtime Owns

| Concern | Description |
|---------|-------------|
| Discovery | Finding extension manifests in filesystem or registry |
| Registry | Deterministic registration of discovered extensions |
| Manifest loading | Parsing and validating `extension.yaml` files |
| Lifecycle management | State machine transitions (8 states) |
| Validation orchestration | Tier 1 (schema) and Tier 2 (dependency) validation |
| Permission enforcement | Granting and checking extension permissions |
| Capability coordination | Registering and resolving extension capabilities |
| CLI integration | Kilo commands for extension management |

### Extensions Own

| Concern | Description |
|---------|-------------|
| Domain capability | The actual capability the extension provides |
| Implementation logic | How the capability works internally |
| Extension-specific contracts | Custom validation, configuration, or behavior |

---

## 3. Extension Manifest Contract

### Required Fields

```yaml
# extension.yaml
extension_id: str          # Unique identifier (e.g., "ecp", "mcp")
name: str                  # Human-readable name
version: str               # Semver (e.g., "0.1.0")
owner: str                 # Responsible team or individual
description: str           # Purpose and scope
runtime_compatibility: str # Semver constraint (e.g., ">=0.1.0,<1.0.0")
```

### Optional Fields

```yaml
dependencies: list[str]       # Extension IDs this extension depends on
capabilities: list[str]       # Capability IDs this extension provides
lifecycle_hooks:              # Optional lifecycle callbacks
  on_install: str
  on_enable: str
  on_disable: str
  on_remove: str
permissions:                  # Required runtime permissions
  - resource: str
    actions: list[str]
entry_point: str              # Python module path
config_schema: dict           # JSON Schema for extension configuration
tags: list[str]               # Classification tags
```

### Contract Validation

Every extension MUST validate against:
1. `schemas/extensions/extension.schema.json` (Draft 2020-12)
2. `contracts/extensions/extension.contract.yaml` (lifecycle rules)
3. `profiles/extensions/extension.validation.yaml` (Tier 1/Tier 2 checks)

---

## 4. Extension Lifecycle

```
install → discover → validate → load → initialize → execute → shutdown → remove
    │         │          │       │        │           │         │         │
    └─── failed ── failed ── failed ── failed ── failed ── failed ── failed
```

### State Table

| State | Description | Valid Transitions |
|-------|-------------|-------------------|
| `INSTALLED` | Package present on filesystem | discover, failed, remove |
| `DISCOVERED` | Manifest parsed, identity known | validate, failed, remove |
| `VALIDATED` | Manifest + dependencies validated | load, failed, remove |
| `LOADED` | Code loaded into runtime | initialize, failed, remove |
| `INITIALIZED` | Extension ready to execute | execute, shutdown, failed |
| `EXECUTING` | Extension actively running | shutdown, failed |
| `SHUTDOWN` | Extension stopped | remove, failed |
| `REMOVED` | Extension uninstalled | (terminal) |
| `FAILED` | Error at any transition | remove, install (retry) |

---

## 5. Extension Dependency Rules

### Allowed

```
extension
    │
    ├── extensions.sdk.*      (Extension SDK — always allowed)
    ├── runtime.api.*          (Runtime Public API — always allowed)
    └── stdlib                 (Standard library — always allowed)
```

### Forbidden

```
extension
    │
    ├── runtime.kernel.*       ✗ (Runtime internals)
    ├── runtime.services.*     ✗ (Service layer)
    ├── runtime/assets/*       ✗ (Direct subsystem access)
    ├── contracts/*            ✗ (Contracts are for runtime definition)
    ├── schemas/*              ✗ (Schemas are for validation)
    └── profiles/*             ✗ (Profiles are for validation)
```

### Dependency Resolution

Dependencies between extensions are declared in `extension.yaml`:

```yaml
dependencies:
  - ecp           # Requires the ECP extension to be loaded first
  - mcp           # Requires the MCP extension
```

The Extension Runtime resolves dependencies topologically before loading.
Circular dependencies are rejected.

---

## 6. Repository Ownership Model

### Extension Runtime

```
runtime/extensions/          → Extension Runtime implementation
    manager.py               → Lifecycle orchestration
    registry.py              → Deterministic registration
    lifecycle.py             → State machine
    loader.py                → Discovery and loading
    validator.py             → Validation orchestration
    permissions.py           → Permission management
    capabilities.py          → Capability coordination
    events.py                → EventBus integration
    snapshot.py              → Immutable state snapshots
    exceptions.py            → Error types
```

### Extension SDK (already exists, LID-0004)

```
extensions/sdk/              → Library consumed by extensions
    extension.py             → Extension Protocol
    manifest.py              → ExtensionManifest model
    lifecycle.py             → SDK lifecycle helpers
    capabilities.py          → Capability registry
    dependencies.py          → Dependency resolution
    loader.py                → SDK loader
    registry.py              → SDK registry
    packaging.py             → Package handling
    compatibility.py         → Version compatibility
    validation.py            → Validation engine
```

### Extension Implementations

```
extensions/<name>/           → Each extension in its own directory
    extension.yaml           → Manifest
    main.py                  → Entry point implementing Extension protocol
    contracts/               → Extension-specific contracts
    schemas/                 → Extension-specific schemas
    tests/                   → Extension-specific tests
    docs/                    → Extension-specific documentation
```

### Contracts and Schemas

| Path | Content |
|------|---------|
| `contracts/extensions/` | Extension contract, lifecycle, permission contracts |
| `schemas/extensions/` | Manifest schema, permission schema |
| `profiles/extensions/` | Validation profile |

### Tests

| Path | Content |
|------|---------|
| `tests/extensions/unit/` | Extension Runtime unit tests |
| `tests/extensions/integration/` | Cross-extension integration tests |

### Documentation

| Path | Content |
|------|---------|
| `docs/extensions/runtime.md` | Extension Runtime documentation |
| `docs/extensions/<name>/` | Per-extension documentation |
| `docs/milestones/M17/` | Milestone documentation |

---

## 7. Versioning Strategy

### Compatibility Matrix

| Component | Version Strategy |
|-----------|-----------------|
| LEP Runtime | `0.x` — frozen baseline, bugfix only |
| Extension Runtime | `0.x` — tracks LEP runtime version |
| Extension SDK | `0.x` — semantic versioning |
| Individual extensions | `0.x` — independent versioning |

### Compatibility Rules

1. **Extension Runtime** declares `runtime_compatibility` in its manifest
   specifying the LEP runtime version range it supports.

2. **Extensions** declare `runtime_compatibility` in their manifests
   specifying the Extension Runtime version range they require.

3. **Breaking changes** to the Extension Runtime require a minor version
   bump. Extensions pin their runtime compatibility accordingly.

4. **The Extension SDK** is versioned independently. Extensions declare
   `min_sdk_version` and `max_sdk_version` in their manifests.

### Version Format

All versions follow strict semver: `MAJOR.MINOR.PATCH`

Runtime compatibility constraints follow Python PEP 440 format:
- `>=0.1.0,<1.0.0`
- `>=0.1.0`
- `==0.1.0`
