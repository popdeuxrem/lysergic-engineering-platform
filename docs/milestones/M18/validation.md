# M18 — ECP Runtime Integration Validation Strategy

**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)

---

## 1. Validation Scope

ECP Runtime Integration validation covers the ECP extension's integration with
the LEP Runtime Platform. It does not re-validate the ECP metamodel itself
(which is governed by ECP's own E0.x acceptance process).

### What We Validate

| Concern | Validation |
|---------|------------|
| Extension manifest | ECP manifest validates against extension schema |
| Extension lifecycle | ECP follows install→discover→validate→load→initialize cycle |
| Import boundary | ECP imports only from `extensions.sdk.*` + `runtime.api.*` |
| Graph semantics | Entity/relationship/reference CRUD operations |
| Graph validation | Acyclic dependency, completeness, consistency |
| Governance events | Events published through `runtime.api.publish_event()` |
| Regression | Existing 891 tests still pass |

### What We Do Not Validate

| Concern | Validated By |
|---------|--------------|
| ECP metamodel correctness | ECP E0.x governance process |
| Constitutional law interpretation | Portfolio Authority |
| Entity schema validity | ECP schema validation |
| Relationship semantics | ECP governance rules |

---

## 2. Tier 1 Validation — Structural Primitives

### Schema Validation

| Check | Schema | Enforcement |
|-------|--------|-------------|
| Entity schema valid | `extensions/ecp/schemas/entity.schema.json` | BLOCK |
| Relationship schema valid | `extensions/ecp/schemas/relationship.schema.json` | BLOCK |
| Reference schema valid | `extensions/ecp/schemas/reference.schema.json` | BLOCK |
| Manifest schema valid | `schemas/extensions/extension.schema.json` | BLOCK |

### Contract Validation

| Check | Contract | Enforcement |
|-------|----------|-------------|
| Lifecycle conformance | `contracts/extensions/extension.contract.yaml` | BLOCK |
| ECP capability contract | `extensions/ecp/contracts/graph.contract.yaml` | BLOCK |
| ECP permission contract | `extensions/ecp/contracts/permission.contract.yaml` | BLOCK |

### Extension Validation

| Check | Description |
|-------|-------------|
| Manifest completeness | extension_id, name, version, owner, runtime_compatibility present |
| Runtime compatibility | ECP version range is compatible with installed Extension Runtime |
| Dependency resolution | All declared dependencies are available |
| Capability uniqueness | No duplicate capability IDs across loaded extensions |

---

## 3. Tier 2 Validation — Graph Integrity

### Entity Consistency

| Check | Description |
|-------|-------------|
| Required fields present | Entity has identity, type, version |
| No duplicate identities | Entity IDs are unique within scope |
| Immutable identity | Entity identity does not change after creation |
| Valid entity type | Entity type is registered in ECP type registry |

### Relationship Consistency

| Check | Description |
|-------|-------------|
| Source exists | Relationship source entity is registered |
| Target exists | Relationship target entity is registered |
| Valid relationship type | Relationship type is registered |
| Cardinality satisfied | Relationship cardinality constraints are met |
| No self-references | Source and target are different entities |

### Reference Resolution

| Check | Description |
|-------|-------------|
| Reference target exists | Referenced entity is available |
| Reference type valid | Reference type matches declared type |
| No dangling references | All references resolve to active entities |

### Graph Integrity

| Check | Description |
|-------|-------------|
| Acyclic | No cycles in dependency graph |
| Complete | All required relationships are present |
| Consistent | No conflicting relationship declarations |

---

## 4. Tests Required

### Unit Tests

| Test Area | Coverage |
|-----------|----------|
| Entity CRUD | Create, read, update, delete |
| Relationship CRUD | Create, read, delete (relationships are immutable) |
| Reference resolution | URN lookup, type resolution |
| Graph validation | Acyclic check, completeness check |
| Extension manifest | Manifest loading and validation |
| Import boundary | AST scan of ECP extension files |

### Integration Tests

| Test Area | Coverage |
|-----------|----------|
| Extension Runtime + ECP | Full lifecycle: install → discover → validate → load → initialize |
| ECP + runtime.api | LEP facade consumption, event publishing |
| ECP + ValidationAPI | Schema validation via platform validator |
| Cross-extension | ECP + other extensions (dependency resolution) |

### Regression Tests

| Test Area | Coverage |
|-----------|----------|
| Existing runtime tests | 891 tests must still pass |
| Existing extension tests | 33 Extension Runtime tests must still pass |
| CLI tests | 21 Kilo CLI tests must still pass |

---

## 5. CI Enforcement

```yaml
# .github/workflows/ecp-validation.yml
name: ECP Runtime Integration Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e .
      - run: python -m ruff check extensions/ecp/
      - run: python -m mypy extensions/ecp/ --explicit-package-bases
      - run: python -m pytest tests/ecp/ -v
      - run: python -m pytest tests/ --ignore=tests/tooling -q
      - run: python -m pytest tests/cli/test_import_boundary.py -v
```

### Quality Gates

| Gate | Required |
|------|----------|
| Ruff clean | PASS |
| Mypy strict | PASS |
| ECP unit tests | ≥80% coverage |
| Integration tests | All integration paths covered |
| Import boundary | No prohibited imports in `extensions/ecp/` |
| Combined regression | 891+ tests pass |
