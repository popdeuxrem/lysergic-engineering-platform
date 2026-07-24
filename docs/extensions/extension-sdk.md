# LEP Extension SDK v1.0

## Overview

The LEP Extension SDK provides the canonical runtime contract between the LEP
Kernel and all platform capabilities. Every extension (AI, MCP, Git, Docker,
Python, ECP, user extensions) implements the Extension Protocol and is managed
through the SDK's lifecycle, registry, and validation systems.

## Architecture

```
Extension
    │
    ▼
ExtensionLoader ──► ExtensionRegistry (state, metadata)
    │                   │
    │                   ▼
    ├──► CapabilityRegistry (capability registration, provider lookup)
    ├──► DependencyResolver (topological ordering, cycle detection)
    ├──► ValidationEngine (Tier 1: manifest, Tier 2: dependencies)
    ├──► CompatibilityChecker (SDK version, dependency version)
    └──► EventBus (ExtensionDiscovered, Validated, Loaded, Ready, Failed, Stopped, Removed)
```

## Modules

| Module | Purpose |
|--------|---------|
| `extension.py` | `Extension` Protocol — the interface every extension implements |
| `manifest.py` | `ExtensionManifest` — identity, version, dependencies, capabilities, permissions |
| `lifecycle.py` | `ExtensionLifecycle` — 8-state machine (DISCOVERED → ... → REMOVED) |
| `capabilities.py` | `CapabilityRegistry` — capability registration, versioned provider resolution |
| `dependencies.py` | `DependencyGraph`, `DependencyResolver` — topological sort, cycle detection, optional deps |
| `loader.py` | `ExtensionLoader` — discover → validate → load → unload → remove |
| `registry.py` | `ExtensionRegistry` — installed extensions with state, health, metadata |
| `packaging.py` | `ExtensionPackage`, `PackageInstaller` — package metadata and installation |
| `compatibility.py` | `CompatibilityChecker` — SDK version and dependency version compatibility |
| `validation.py` | `ValidationEngine` — Tier 1 (manifest schema), Tier 2 (dependency graph) |

## Extension Lifecycle

```
DISCOVERED → VALIDATED → LOADING → READY → STOPPING → STOPPED → REMOVED
                │                      │
                ▼                      ▼
              FAILED ←────────────────┘
                │
                ▼
              REMOVED
```

## Events

The SDK publishes the following events (via `EventBus`):

- `extension.ExtensionDiscovered`
- `extension.ExtensionValidated`
- `extension.ExtensionLoaded`
- `extension.ExtensionReady`
- `extension.ExtensionFailed`
- `extension.ExtensionStopped`
- `extension.ExtensionRemoved`

## Validation Tiers

**Tier 1 — Manifest Schema**
- extension_id, name, version required
- SDK version compatibility check
- Entry point advisory warning

**Tier 2 — Dependency Graph**
- Acyclic dependency graph
- Capability provider conflict detection
- Lifecycle transition correctness

## Constraints

- No hidden global state
- No extension-specific logic in the SDK
- Standard library only (stdlib + existing Platform Services interfaces)
- Deterministic, idempotent, typed
