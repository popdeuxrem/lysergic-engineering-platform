# M16 — Kilo CLI Validation Strategy

**Architecture Baseline:** LEP-ARCH-v0.1.0 (Frozen)

---

## 1. Validation Scope

Kilo CLI validation confirms that the CLI is a correct consumer of the
frozen LEP Runtime. It does not re-validate the runtime itself (M15).

### What We Validate

| Concern | Validation |
|---------|------------|
| Command registration | Every command maps to a valid runtime API method |
| Argument parsing | Required args present, types correct |
| Output formatting | JSON/YAML/text output is well-formed |
| Error handling | All runtime exceptions produce valid CLI errors |
| Adapter lifecycle | initialize/shutdown succeeds |
| Import boundary | No prohibited runtime imports (AST-based scan) |

### What We Do Not Validate

| Concern | Validated By |
|---------|--------------|
| Runtime logic | M15 runtime tests (837 tests) |
| Contract conformance | Runtime contract tests |
| Schema validity | Runtime schema tests |
| Lifecycle correctness | Runtime lifecycle tests |
| State machine transitions | Runtime lifecycle tests |

---

## 2. Test Strategy

### Unit Tests

Each command handler is tested using a mock LEP adapter.

| Test Area | Coverage |
|-----------|----------|
| Command handler per command | Every leaf command (version, doctor, inspect, validate) |
| Output formatting | JSON parseable, text readable |
| Error wrapping | All error codes produce correct output |
| Adapter initialize | Success path, not-initialized guard |

### Import Boundary Tests

Every `.py` file under `cli/kilo/` is scanned with AST static analysis.
No file may import from internal runtime modules.

```python
PROHIBITED_IMPORTS = [
    "runtime.kernel", "runtime.services",
    "runtime.assets", "runtime.ai", "runtime.workflows",
    "runtime.plugins", "runtime.projects", "runtime.knowledge",
    "runtime.automation", "runtime.operations", "runtime.configuration",
    "runtime.telemetry", "runtime.validator",
    "contracts", "schemas", "profiles", "extensions", "apps",
]
```

The adapter is the sole bridge. It imports exclusively from `runtime.api`
via `create_default_lep()`. This is verified by a dedicated AST test.

---

## 3. Command Contract Tests

For each command, validate:

```python
COMMAND_CONTRACTS = {
    "version": {
        "runtime_method": "LEP.version()",
        "output_fields": ["platform", "version", "architecture"],
    },
    "doctor": {
        "runtime_method": "DiagnosticsAPI.snapshot()",
        "output_fields": ["ready", "health", "services", "lifecycle"],
    },
    "inspect": {
        "runtime_method": "RuntimeAPI.summary(), DiagnosticsAPI.telemetry_summary()",
        "output_fields": ["platform", "telemetry", "services", "status"],
    },
    "validate": {
        "runtime_method": "DiagnosticsAPI.snapshot()",
        "output_fields": ["valid", "ready", "health", "issues"],
    },
}
```

---

## 4. Dependency Model (Final)

```
cli/kilo
    │
    ├── runtime.api (LEP, create_default_lep)
    │
    └── Standard library (argparse, json, sys, typing)

No CLI component depends on:
    runtime.kernel       ✗
    runtime.services     ✗
    runtime.<subsystem>  ✗
    contracts/schemas    ✗
```

The adapter is the sole bridge between Kilo and the runtime. It imports
only `runtime.api` — specifically `LEP` and `create_default_lep()`.
`create_default_lep()` is a public API factory that internally constructs
the necessary services; Kilo never touches service internals.

---

## 5. CI Integration

```yaml
# .github/workflows/kilo-validation.yml
name: Kilo CLI Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e .  # includes runtime + cli
      - run: python -m ruff check cli/kilo/
      - run: python -m mypy cli/kilo/ --explicit-package-bases
      - run: python -m pytest tests/cli/ -v
      - run: python -m pytest tests/ --ignore=tests/tooling -q
```

---

## 6. Quality Gates

| Gate | Required |
|------|----------|
| Ruff clean | PASS |
| Mypy strict (production code) | PASS |
| Unit tests (CLI) | 21 tests |
| Combined runtime tests | 837 tests |
| Import boundary (AST scan) | No prohibited imports |
| Adapter boundary | Only `runtime.api` |
