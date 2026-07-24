# M17 — Extension Runtime v0.1.0-alpha Release Criteria

**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)
**Target:** `extension-runtime-v0.1.0-alpha`

---

## 1. Release Scope

### Package

```
extension-runtime==0.1.0a1
```

### Components

| Component | Status |
|-----------|--------|
| Extension Runtime (`runtime/extensions/`) | To be implemented |
| Kilo CLI extension commands | To be implemented |
| Extension SDK (`extensions/sdk/`) | Already exists (LID-0004) |
| Extension contract | Already exists |
| Extension schema | Already exists |
| Extension validation profile | Already exists |

### Entry Points (CLI)

```
lep extension install <path>     # Install extension from filesystem
lep extension list               # List installed extensions
lep extension info <id>          # Show extension details
lep extension enable <id>        # Enable extension
lep extension disable <id>       # Disable extension
lep extension remove <id>        # Remove extension
```

---

## 2. Release Criteria

### Architecture Compliance

| Criterion | Requirement | Verification |
|-----------|-------------|--------------|
| No runtime internals | `runtime/extensions/*` imports only from `runtime.api` + `extensions.sdk` | AST-based import boundary test |
| Extension isolation | Extensions consume `extensions.sdk.*` and `runtime.api.*` only | Architecture review |
| Runtime not modified | `runtime/` (outside `runtime/extensions/`) has zero changes | `git diff` |
| Layer hierarchy preserved | CLI → Extension Runtime → SDK → Runtime API | Dependency analysis |

### Functionality

| Criterion | Requirement |
|-----------|-------------|
| Extension registry | Register, unregister, get, list, freeze operational |
| Lifecycle management | All 8 states reachable via valid transitions |
| Dependency resolution | Topological ordering, cycle detection |
| Permission enforcement | Grant/deny by default, strict mode |
| Capability coordination | Registration, conflict detection |
| Event integration | All lifecycle events published via EventBus |
| CLI integration | All extension commands delegate correctly |

### Quality

| Criterion | Requirement |
|-----------|-------------|
| Ruff clean | `ruff check runtime/extensions/` passes |
| Mypy strict | `mypy runtime/extensions/ --explicit-package-bases` passes |
| Unit tests | ≥70% coverage |
| Integration tests | Extension Runtime + SDK, + CLI, + EventBus |
| Import boundary | AST-scan — no prohibited imports |
| Combined regression | Existing 858+ tests still pass |
| Extension SDK tests | Existing 82 tests still pass |

---

## 3. Dependencies (Pre-existing)

| Component | Location | Tests | Status |
|-----------|----------|-------|--------|
| Extension SDK | `extensions/sdk/` | 82 | ✅ Complete |
| Extension contract | `contracts/extensions/extension.contract.yaml` | — | ✅ Complete |
| Extension schema | `schemas/extensions/extension.schema.json` | — | ✅ Complete |
| Extension profile | `profiles/extensions/extension.validation.yaml` | — | ✅ Complete |
| LEP Runtime | `runtime/` | 837 | ✅ Frozen |
| Kilo CLI | `cli/kilo/` | 21 | ✅ Alpha |

---

## 4. Release Process

```
1. Runtime implementation → runtime/extensions/ modules
2. CLI commands          → Kilo extension command group
3. Tests complete        → Unit + integration + regression pass
4. Boundary verified     → Import boundary test passes
5. Review complete       → Architecture review
6. Tag                  → git tag -a extension-runtime-v0.1.0-alpha
```

---

## 5. Post-Release Roadmap

| Phase | Scope |
|-------|-------|
| `extension-runtime-v0.1.0a1` | Core runtime + CLI (current) |
| `extension-runtime-v0.1.0a2` | ECP Runtime extension |
| `extension-runtime-v0.1.0a3` | MCP integration |
| `extension-runtime-v0.1.0` | Stable release |

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Extension SDK API changes | Low (already shipped) | High | Pin SDK version in runtime |
| Runtime API missing required interface | Medium | Medium | Add to `runtime.api.*` if justified |
| Extension discovery slow | Medium | Low | Cache manifests, lazy loading |
| Permission model too restrictive | Low | Medium | Configurable strict mode |
| Extension conflicts (capability overlap) | Medium | Medium | Capability priority/version negotiation |

---

## 7. Release Checklist

- [ ] `runtime/extensions/` implemented
- [ ] Kilo extension CLI commands implemented
- [ ] AST import boundary test passes
- [ ] `ruff check runtime/extensions/` passes
- [ ] `mypy runtime/extensions/` passes
- [ ] Extension Runtime unit tests pass
- [ ] Integration tests pass
- [ ] Combined regression tests pass (858+)
- [ ] `git diff runtime/` shows only `runtime/extensions/` changes
- [ ] Architecture review completed
- [ ] Tag `extension-runtime-v0.1.0-alpha` created
