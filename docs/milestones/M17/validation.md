# M17 — Extension Runtime Validation Strategy

**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)

---

## 1. Validation Scope

Extension Runtime validation covers the runtime layer that manages extensions.
It does not validate individual extension implementations (that is the
extension author's responsibility).

### What We Validate

| Concern | Validation |
|---------|------------|
| Manifest schema | Extension manifests validate against Draft 2020-12 schema |
| Registry operations | Register, unregister, get, list, freeze |
| Lifecycle transitions | All 8-state transitions are correct |
| Dependency resolution | Topological ordering, cycle detection |
| Permission enforcement | Grant/deny logic, strict mode |
| Capability coordination | Registration, conflict detection |
| CLI integration | Kilo commands delegate correctly |
| Import boundary | Extension Runtime imports only from allowed modules |

### What We Do Not Validate

| Concern | Validated By |
|---------|--------------|
| Individual extension logic | Extension author |
| Runtime internals | M15 runtime tests (837 tests) |
| Extension SDK internals | LID-0004 tests (82 tests) |
| Contract conformance | Contract test suite |

---

## 2. Manifest Schema Validation

Every extension manifest MUST validate against:

1. `schemas/extensions/extension.schema.json` — Draft 2020-12 structure
2. `contracts/extensions/extension.contract.yaml` — Lifecycle conformance
3. `profiles/extensions/extension.validation.yaml` — Tier 1/Tier 2 rules

### Schema Checks

| Rule ID | Check | Enforcement |
|---------|-------|-------------|
| `ext-validate-manifest-schema` | Manifest is valid Draft 2020-12 | BLOCK |
| `ext-metadata-completeness` | All required fields present | BLOCK |
| `ext-identity-format` | Extension ID follows naming convention | BLOCK |
| `ext-sdk-compatibility` | SDK version range is compatible | WARN |
| `ext-permission-format` | Permissions follow schema | BLOCK |

---

## 3. Registry Validation

| Test | Description |
|------|-------------|
| Register extension | Extension added to registry |
| Register duplicate | Duplicate ID raises ConflictError |
| Get by ID | Identity lookup returns correct manifest |
| List all | Returns all registered extensions |
| Unregister | Extension removed from registry |
| Freeze | Registry rejects new registrations after freeze |
| List by capability | Filter by capability ID |
| List by state | Filter by lifecycle state |

---

## 4. Lifecycle Validation

### State Machine Tests

| Test | From | To | Expected |
|------|------|----|----------|
| Install | (none) | INSTALLED | OK |
| Discover | INSTALLED | DISCOVERED | OK |
| Validate | DISCOVERED | VALIDATED | OK |
| Load | VALIDATED | LOADED | OK |
| Initialize | LOADED | INITIALIZED | OK |
| Execute | INITIALIZED | EXECUTING | OK |
| Shutdown | INITIALIZED | SHUTDOWN | OK |
| Shutdown | EXECUTING | SHUTDOWN | OK |
| Remove | SHUTDOWN | REMOVED | OK |
| Remove | INSTALLED | REMOVED | OK |
| Invalid transition | DISCOVERED | EXECUTING | REJECTED |

---

## 5. Dependency Validation

| Test | Description |
|------|-------------|
| No dependencies | Single extension loads correctly |
| Linear dependency | A→B loads B before A |
| Diamond dependency | A→B, A→C, B→D, C→D loads correctly |
| Circular dependency | A→B→A raises cycle error |
| Missing dependency | A requires B, B absent — rejected |
| Optional dependency | A requires B (optional), B absent — allowed |

---

## 6. Compatibility Testing

| Test | Description |
|------|-------------|
| SDK version match | Extension SDK version within range |
| SDK version too high | Extension requires newer SDK — rejected |
| SDK version too low | Extension requires older SDK — allowed |
| Runtime version match | Extension runtime compatibility satisfied |
| Runtime version mismatch | Extension incompatible — rejected |

---

## 7. Integration Testing

| Integration | Purpose |
|-------------|---------|
| Extension Runtime + EventBus | Lifecycle events published correctly |
| Extension Runtime + Kilo CLI | CLI commands trigger correct runtime operations |
| Extension Runtime + Extension SDK | Runtime delegates to SDK correctly |
| Extension Runtime + Runtime API | Extensions consume API via allowed paths |

---

## 8. CI Enforcement Strategy

```yaml
# .github/workflows/extension-runtime-validation.yml
name: Extension Runtime Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e .  # runtime + sdk + cli
      - run: python -m ruff check runtime/extensions/
      - run: python -m mypy runtime/extensions/ --explicit-package-bases
      - run: python -m pytest tests/extensions/ -v
      - run: python -m pytest tests/ --ignore=tests/tooling -q  # regression
```

### Quality Gates

| Gate | Required |
|------|----------|
| Ruff clean | PASS |
| Mypy strict | PASS |
| Extension Runtime unit tests | ≥80% coverage |
| Integration tests | All integration paths covered |
| Import boundary | No prohibited runtime imports |
| Combined regression | 858+ tests pass |
