# LEP Asset Runtime v1.0

## Overview

The LEP Asset Runtime introduces a governed asset management layer for
engineering artifacts. Assets are first-class runtime objects with identity,
type, version, metadata, ownership, location, dependencies, validation state,
and lifecycle state.

## Architecture

```
AssetManager (orchestrator)
  ├── AssetRegistry     — deterministic registration, type/version lookup
  ├── AssetLifecycle    — REGISTERED → VALIDATED → AVAILABLE → DEPRECATED → REMOVED
  ├── AssetCatalog      — discovery metadata indexing and filtering
  ├── AssetDependencyGraph  — dependency ordering, cycle detection
  ├── AssetValidator    — Tier 1 (schema/metadata), Tier 2 (dependency/compat)
  ├── AssetResolver     — URN resolution, identity-based lookup
  ├── AssetSearch       — metadata-based text search
  ├── AssetCache        — deterministic caching with explicit invalidation
  ├── AssetLoader       — pluggable content loading providers
  ├── AssetSnapshot     — immutable state snapshots
  └── AssetEventPublisher   — EventBus integration
```

## Asset Lifecycle

```
REGISTERED → VALIDATED → AVAILABLE → DEPRECATED → REMOVED
    │            │            │
    └── REMOVED  └── REMOVED  └── REMOVED
                 └── DEPRECATED
                               └── AVAILABLE (reactive)
```

## Asset Metadata

| Field | Required | Type |
|-------|----------|------|
| asset_id | yes | string |
| asset_type | yes | string |
| version | yes | string (semver) |
| owner | no | string |
| description | no | string |
| tags | no | tuple[string] |
| checksum | no | string |
| origin | no | string |

## Key Operations

- `register(metadata)` — register a new asset
- `get(asset_id)` — retrieve by identity (cached)
- `list(asset_type)` — list all or filtered
- `validate(asset_id)` — Tier 1 validation, transition to VALIDATED
- `activate(asset_id)` — transition to AVAILABLE
- `deprecate(asset_id)` — transition to DEPRECATED
- `remove(asset_id)` — remove from registry
- `search_assets(query)` — metadata text search
- `resolve_urn(urn)` — URN-based resolution
- `snapshot_state()` — immutable state snapshot

## Events

- `asset.AssetRegistered`
- `asset.AssetValidated`
- `asset.AssetAvailable`
- `asset.AssetDeprecated`
- `asset.AssetRemoved`
- `asset.AssetFailed`

## Validation Tiers

**Tier 1:**
- Schema validation (Draft 2020-12)
- Metadata completeness
- Identity format

**Tier 2:**
- Dependency graph (acyclic)
- Version compatibility
- Ownership validation

## Providers

Asset content can be loaded through pluggable providers:
- `RepositoryProvider` — local filesystem

Future providers can implement the `AssetLoaderProvider` protocol.

## Integration Points

- **EventBus** — lifecycle events published during transitions
- **Configuration Runtime** — provider configuration via layered config
- **Extension SDK** — extensions may expose assets for resolution
- **Core API** — `AssetsAPI` facade in `runtime/api/`
