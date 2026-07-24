# M18 — ECP Runtime Integration v0.1.0-alpha Release Criteria

**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)
**Target:** `ecp-runtime-v0.1.0-alpha`
**ECP Baseline:** ECP-RP-v0.1.0 (Accepted governance artifacts)

---

## 1. Release Scope

### Package

```
ecp-runtime==0.1.0a1
```

### Components

| Component | Location | Status |
|-----------|----------|--------|
| ECP Extension | `extensions/ecp/` | To be implemented |
| ECP schemas | `extensions/ecp/schemas/` | To be created |
| ECP contracts | `extensions/ecp/contracts/` | To be created |
| ECP tests | `tests/ecp/` | To be created |
| Extension Runtime | `runtime/extensions/` | ✅ Complete (M17) |
| Extension SDK | `extensions/sdk/` | ✅ Complete (LID-0004) |
| LEP Runtime | `runtime/` | ✅ Frozen (M15) |

### Dependencies (Pre-existing)

| Component | Location | Tests | Status |
|-----------|----------|-------|--------|
| LEP Runtime | `runtime/` | 858 | ✅ Frozen |
| Extension Runtime | `runtime/extensions/` | 33 | ✅ Alpha |
| Extension SDK | `extensions/sdk/` | 82 | ✅ Complete |
| Kilo CLI | `cli/kilo/` | 21 | ✅ Alpha |

---

## 2. Release Criteria

### Architecture Compliance

| Criterion | Requirement | Verification |
|-----------|-------------|--------------|
| No runtime internals | `extensions/ecp/*` imports only from `runtime.api.*` + `extensions.sdk.*` | AST-based import boundary test |
| Extension lifecycle | ECP follows M17 lifecycle (install→discover→validate→load→initialize) | Extension Runtime test |
| LEP hierarchy preserved | ECP is consumed as extension, not platform root | Architecture review |
| Runtime not modified | `runtime/` has zero changes | `git diff runtime/` |
| ECP model preserved | L0/L1/L2 separation maintained, no concept merging | Code review |

### Functionality

| Criterion | Requirement |
|-----------|-------------|
| Entity management | Create, read, update governed entities |
| Relationship management | Create, read typed relationships between entities |
| Reference resolution | URN-based lookup resolves to entities |
| Graph validation | Acyclic dependency, completeness, consistency checks |
| Event integration | Governance events published via `runtime.api.publish_event()` |
| Manifest validation | ECP manifest validates correctly |

### Quality

| Criterion | Requirement |
|-----------|-------------|
| Ruff clean | `ruff check extensions/ecp/` passes |
| Mypy strict | `mypy extensions/ecp/ --explicit-package-bases` passes |
| ECP unit tests | ≥80% coverage |
| Graph validation tests | All graph rules tested |
| Import boundary | AST-scan — no prohibited imports |
| Combined regression | Existing 891 tests still pass |

---

## 3. ECP Extension Structure

```
extensions/ecp/
    extension.yaml              # ECP manifest
    adapter.py                  # Runtime entry point
    lifecycle.py                # Lifecycle hooks
    graph/
        __init__.py
        entities.py             # Entity management
        relationships.py        # Relationship management
        references.py           # Reference resolution
        validator.py            # Graph validation
    schemas/
        entity.schema.json      # Entity Draft 2020-12 schema
        relationship.schema.json # Relationship Draft 2020-12 schema
        reference.schema.json   # Reference Draft 2020-12 schema
    contracts/
        graph.contract.yaml     # Graph semantics contract
        permission.contract.yaml # Permission contract
    tests/
        unit/
            test_entities.py
            test_relationships.py
            test_references.py
            test_validator.py
            test_adapter.py
        integration/
            test_ecp_lifecycle.py
```

---

## 4. Release Process

```
1. ECP extension implementation   → extensions/ecp/ modules
2. Schemas and contracts          → Draft 2020-12 + contract YAML
3. Tests complete                 → Unit + integration + regression pass
4. Boundary verified              → AST import boundary test passes
5. Review complete                → Architecture + ECP governance review
6. Tag                            → git tag -a ecp-runtime-v0.1.0-alpha
```

---

## 5. Post-Release Roadmap

| Phase | Scope |
|-------|-------|
| `ecp-runtime-v0.1.0a1` | Core graph semantics + entity/relationship management (current) |
| `ecp-runtime-v0.1.0a2` | Constitutional invariant enforcement (Law 0, dependency/ownership invariants) |
| `ecp-runtime-v0.1.0a3` | Kilo CLI ECP commands (`lep ecp` subcommands) |
| `ecp-runtime-v0.1.0` | Stable release |

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ECP schema conflicts with frozen runtime schemas | Low | High | ECP schemas are extension-scoped, not platform-scoped |
| Graph validation performance | Medium | Medium | Optimize validation for typical graph sizes |
| Constitutional invariant enforcement conflicts | Low | Medium | ECP governance rules are ECP's responsibility; LEP provides runtime |
| Extension SDK API gaps | Medium | Medium | Add to `extensions.sdk.*` or `runtime.api.*` if justified |

---

## 7. Release Checklist

- [ ] `extensions/ecp/` implemented with all modules
- [ ] ECP schemas created (entity, relationship, reference)
- [ ] ECP contracts created (graph, permission)
- [ ] AST import boundary test covers `extensions/ecp/`
- [ ] `ruff check extensions/ecp/` passes
- [ ] `mypy extensions/ecp/` passes
- [ ] ECP unit tests pass
- [ ] Integration tests pass
- [ ] Combined regression tests pass (891+)
- [ ] `git diff runtime/` is empty (frozen baseline preserved)
- [ ] Architecture review completed
- [ ] ECP governance review completed
- [ ] Tag `ecp-runtime-v0.1.0-alpha` created

---

## 8. Rollback Considerations

| Scenario | Rollback Action |
|----------|-----------------|
| ECP extension fails to initialize | Extension Runtime disables extension, reports FAILED state |
| Graph validation regression | Disable ECP extension, revert to prior version |
| Runtime API incompatibility | Pin ECP extension to compatible runtime version |
| Schema conflict | ECP schemas are extension-scoped; uninstall extension to remove |
