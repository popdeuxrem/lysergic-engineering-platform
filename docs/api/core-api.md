# LEP Core API v1.0

## Overview

The LEP Core API is the canonical facade layer exposing platform functionality
to clients, extensions, automation workflows, and user interfaces. It is a
thin orchestration layer containing zero business logic. All operations
delegate to Platform Services, Runtime Kernel components, or registered
runtime services.

## Architecture

```
Client / Extension / CLI / UI
            │
            ▼
   ┌───────────────┐
   │  LEP Facade   │  ← Single entry point, pure delegation
   └───────┬───────┘
           │
   ┌───────┴───────┐
   │  8 Domains    │  ← Domain-specific facades
   ├───────────────┤
   │  runtime      │  Platform identity, version, architecture, status
   │  extensions   │  Discovery, registration, enable/disable, install
   │  projects     │  Lifecycle, workspace, search, update
   │  assets       │  Discovery (schemas, templates, contracts, profiles)
   │  knowledge    │  Sources, entries, indexing, search
   │  workflows    │  Lifecycle, execution, scheduling, history
   │  validation   │  Schema/contract/profile validation, aggregated reports
   │  diagnostics  │  Health, snapshots, telemetry, errors
   └───────┬───────┘
           │
   ┌───────┴───────┐
   │  Platform     │  ← ServiceManager, EventBus, HealthService, etc.
   │  Services     │
   └───────────────┘
```

## LEP Facade

The top-level `LEP` class composes all 8 domain facades:

```python
from runtime.api import LEP

lep = LEP(service_manager)

# Start/stop the platform
lep.start()
lep.stop()

# Access domains
lep.runtime.platform_name()    # "Lysergic Engineering Platform"
lep.extensions.enable("ext-1")
lep.projects.create("p1", "Project 1")
lep.validation.validate_schema(schema, instance)
lep.diagnostics.snapshot()
```

## Domain Reference

### Runtime API
- `platform_name()`, `platform_version()` — platform identity
- `architecture_id()`, `architecture_status()` — architecture info
- `schema_dialect()` — validation dialect
- `service_ids()`, `service_count()` — service discovery
- `runtime_status()` — health, lifecycle, readiness
- `uptime()` — runtime duration
- `summary()` — aggregated platform info

### Extensions API
- `register(id, name, version)` — register an extension
- `install(id, source)` — install from source path
- `enable(id)`, `disable(id)` — lifecycle control
- `is_enabled(id)` — status check
- `list()`, `list_by_state(state)` — discovery
- `get(id)`, `remove(id)` — lookup and removal
- `metadata()` — aggregated extension metadata

### Projects API
- `create(id, name)` — create new project
- `get(id)`, `list()` — discovery
- `search(query)` — text search (name, ID, description)
- `update(id, **kwargs)` — mutate name/version/description/workspace
- `remove(id)`, `count()` — lifecycle

### Assets API
- `store(id, type)` — store schemas, templates, contracts, profiles
- `get(id)`, `list(type)` — discovery
- `list_by_type(type)`, `list_types()` — typed listing
- `search(query)` — text search across ID, description, tags
- `tag(id, tags)` — add tags to asset
- `remove(id)`, `count(type)`

### Knowledge API
- `register_source(id, name)` — register knowledge sources
- `sources()` — list registered sources
- `add(id, kind, content)` — add knowledge entry
- `get(id)`, `search(kind, tag, query)` — discovery
- `index(id)` — mark entry as indexed
- `remove(id)`, `count(kind)`

### Workflows API
- `create(id, name, steps)` — create workflow
- `get(id)`, `list(status)` — discovery
- `start(id)`, `complete(id)` — execution
- `fail(id, error)`, `cancel(id)` — error/abort
- `schedule(id, datetime)` — scheduled execution
- `history()`, `list_scheduled()` — historical tracking
- `count()`

### Validation API
- `validate_schema(schema, instance)` — schema validation
- `validate_contract(contract, instance)` — contract validation
- `validate_profile(profile, instance)` — profile validation
- `aggregated_report(checks)` — batch validation report
- `set_validator(validator)` — configure validator
- `dialect`, `is_validator_set()` — validator status

### Diagnostics API
- `snapshot()` — full runtime snapshot (health, services, lifecycle, errors)
- `record_error(source, message)` — record diagnostic error
- `clear_errors()` — clear error log
- `telemetry_summary()` — event bus and subscriber metrics
- `service_count`, `list_service_ids()` — service discovery
- `is_healthy()` — platform readiness check

## Testing Coverage

- **Unit tests:** Every public method across all 8 domains
- **Integration tests:** Cross-domain composition, full lifecycles
- **Delegation tests:** LEP facade delegates correctly to each domain
- **Edge cases:** Missing entities, state guard transitions, shutdown idempotence
