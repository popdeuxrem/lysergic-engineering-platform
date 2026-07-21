# Build Automation Foundation

## Overview

M2.4 establishes deterministic engineering validation automation, evidence collection, and artifact governance checks.

## Validation Workflow

The validation workflow consists of three scripts:

1. **`scripts/validate.sh`** — Deterministic validation entry point
2. **`scripts/capture-evidence.sh`** — Evidence capture producing artifacts
3. **`scripts/validate-manifest.py`** — Read-only manifest validation

### Usage

```bash
# Run full validation
./scripts/validate.sh

# Run validation and capture evidence
./scripts/capture-evidence.sh

# Validate manifest only
python3 scripts/validate-manifest.py
```

### Validation Steps

The validation runner executes:

1. `uv sync` — dependency resolution
2. `uv run pytest` — test suite
3. `uv run ruff check .` — linting
4. `uv run mypy src` — type checking
5. `docker build .` — container build

Each step must pass before the next executes.

## Evidence Locations

Evidence is captured to:

```
docs/validation/artifacts/M2.4/
├── repository-status.txt
├── validation-run.txt
├── pytest.txt
├── ruff.txt
├── mypy.txt
├── docker-build.txt
└── manifest-validation.txt
```

## Safety Constraints

The automation layer does **not**:

- Commit or push changes
- Modify source code or runtime
- Create or approve capabilities
- Perform autonomous fixes
- Transition lifecycle states

All operations are read-only validation and evidence capture.
