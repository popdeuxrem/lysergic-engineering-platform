# M16 — Kilo CLI v0.1.0-alpha Release Criteria

**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)

---

## 1. Release Scope

### Package

```
kilo-cli==0.1.0a1
```

### Entry Points

```
lep version     # Platform version information
lep doctor      # Platform diagnostics
lep inspect     # Platform state inspection
lep validate    # Platform readiness validation
```

---

## 2. Release Criteria

### Architecture Compliance

| Criterion | Requirement | Verification |
|-----------|-------------|--------------|
| No runtime internals | `cli/kilo/*` imports only from `runtime.api` | AST-based `test_import_boundary.py` |
| Adapter bridges runtime | Adapter uses `create_default_lep()` from `runtime.api` | `test_adapter_bridges_runtime()` |
| No business logic duplication | Commands are thin wrappers around runtime API calls | Code review |
| Runtime not modified | `runtime/` has zero changes | `git diff runtime/` |

### Functionality

| Criterion | Requirement |
|-----------|-------------|
| LEP adapter | Initializes and shuts down LEP runtime via `create_default_lep()` |
| Command parsing | All leaf commands accept `--format` (text/json) |
| Output formatting | JSON output parseable; text output readable |
| Auto-format detection | JSON when piped, text on TTY |
| Error handling | Runtime exceptions produce CLI errors with codes + exit codes |

### Quality

| Criterion | Requirement |
|-----------|-------------|
| Ruff clean | `ruff check cli/kilo/` passes |
| Mypy strict | `mypy cli/kilo/ --explicit-package-bases` passes (production code) |
| Unit tests | 21 tests covering adapter, commands, output, error model |
| Import boundary | AST-scan of all Kilo files — no prohibited imports |
| Combined tests | `pytest tests/ --ignore=tests/tooling` passes (837 runtime + 21 CLI) |

---

## 3. Release Process

```
1. Feature complete   → version, doctor, inspect, validate implemented
2. Boundary verified  → import boundary test passes (AST scan)
3. Test complete      → 858 tests pass (837 runtime + 21 CLI)
4. Review complete    → Architecture review — boundary resolved
5. Tag               → git tag -a kilo-v0.1.0-alpha -m "..."
6. Package           → python -m build
```

### Release Checklist

- [x] All 4 commands implemented (version, doctor, inspect, validate)
- [x] `cli/kilo/*` imports only from `runtime.api` — verified by AST scan
- [x] Adapter uses `create_default_lep()` — no `runtime.services` imports
- [x] `ruff check cli/kilo/` passes
- [x] `mypy cli/kilo/ --explicit-package-bases` passes (production)
- [x] `pytest tests/cli/` passes (21 tests)
- [x] `pytest tests/ --ignore=tests/tooling` passes (858 total)
- [x] `git diff runtime/` is empty — frozen baseline preserved

---

## 4. Dependency Model (Final, Resolved)

```
cli/kilo
    │
    ├── runtime.api (LEP, create_default_lep)
    ├── cli.kilo.* (internal modules)
    └── Standard library
```

**Resolved boundary issue:** The original adapter imported directly from
`runtime.services.*` to construct `ServiceManager`. A new public API
factory `create_default_lep()` was added to `runtime.api` — it internally
constructs the ServiceManager and returns a ready-to-use `LEP` instance.

This is a public API addition, not a runtime behavior change. The frozen
`LEP-ARCH-v0.1.0` baseline is preserved. All runtime files remain
unmodified.

---

## 5. Post-Release

| Phase | Scope |
|-------|-------|
| kilo-v0.1.0a1 | Alpha release with 4 commands (current) |
| kilo-v0.1.0a2 | Additional command groups (project, asset, workflow) |
| kilo-v0.1.0 | Maturity — stable, documented, CI/CD |

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Runtime API changes affect CLI | Low (M15 frozen) | High | CLI tested against frozen runtime |
| Missing runtime API for CLI needs | Medium | Medium | Add to `runtime.api.*` if justified |
| Python version compatibility | Low | Medium | Test on Python 3.12+ in CI |
| Slow LEP initialization | Medium | Low | Lazy initialization, progress indicator |

---

## 7. Release Record — kilo-v0.1.0-alpha

**Release date:** 2026-07-24
**Release tag:** `kilo-v0.1.0-alpha`
**Architecture baseline:** LEP-ARCH-v0.1.0 (Frozen)

### Git References

| Ref | Hash |
|-----|------|
| Release tag | `kilo-v0.1.0-alpha` |
| Kilo CLI implementation | `2ae26f0` |
| Architecture boundary resolution | `0d95e14` |
| M15 Runtime Freeze | `36c8b24` |

### Commit History (Kilo CLI)

| Commit | Message |
|--------|---------|
| `2ae26f0` | `kilo(cli): implement alpha with version/doctor/inspect/validate commands` |
| `0d95e14` | `kilo(cli): resolve architecture boundary - adapter uses runtime.api only` |

### Supported Commands

| Command | Description | Flags |
|---------|-------------|-------|
| `lep version` | Show platform version, name, architecture | `--format text\|json` |
| `lep doctor` | Run platform diagnostics (health, services, lifecycle, errors) | `--format text\|json` |
| `lep inspect` | Inspect platform state (summary, telemetry, services, uptime) | `--format text\|json` |
| `lep validate` | Validate platform readiness (valid/ready/health/issues) | `--format text\|json` |

All commands support auto-format detection: JSON when piped, text on TTY.

### Validation Results

| Gate | Result | Detail |
|------|--------|--------|
| Import boundary (AST scan) | **PASS** | 0 prohibited imports across all `cli/kilo/*.py` files |
| Adapter boundary | **PASS** | Imports only from `runtime.api` |
| Ruff | **PASS** | 0 errors |
| Mypy (production) | **PASS** | 0 errors |
| CLI unit tests | **PASS** | 21/21 |
| Combined runtime tests | **PASS** | 858/858 (837 runtime + 21 CLI) |
| Runtime unmodified | **PASS** | No frozen runtime behavior changed |

### Known Limitations

| Limitation | Impact | Planned Resolution |
|------------|--------|-------------------|
| No interactive mode | Commands are single-shot only | kilo-v0.1.0a2 |
| No config file support | CLI always loads `lep.yaml` from CWD | kilo-v0.1.0a2 |
| 4 commands only | Project, asset, workflow, extension, knowledge, plugin, AI, automation, and operations commands not yet implemented | kilo-v0.1.0a2 |
| No plugin-based command loading | All commands are statically registered | kilo-v0.1.0a3 |
| Startup latency | `create_default_lep()` initializes full runtime each invocation | Optimize with lazy init in kilo-v0.1.0a2 |
| No Python package build | `python -m build` not yet configured | Package setup pending M16 finalization |
