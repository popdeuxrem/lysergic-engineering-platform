#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../apps/api/control-plane" && pwd)"
ARTIFACTS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/docs/validation/artifacts/M2.4"

log() {
    echo "[capture] $*"
}

mkdir -p "$ARTIFACTS_DIR"

log "Capturing repository status..."
git status > "$ARTIFACTS_DIR/repository-status.txt" 2>&1

log "Running validation and capturing output..."
"$SCRIPT_DIR/validate.sh" > "$ARTIFACTS_DIR/validation-run.txt" 2>&1

log "Capturing individual test outputs..."
cd "$PROJECT_DIR"

uv run pytest > "$ARTIFACTS_DIR/pytest.txt" 2>&1 || true
uv run ruff check . > "$ARTIFACTS_DIR/ruff.txt" 2>&1 || true
uv run mypy src > "$ARTIFACTS_DIR/mypy.txt" 2>&1 || true
docker build . -t lep-control-plane:evidence > "$ARTIFACTS_DIR/docker-build.txt" 2>&1 || true

log "Validating manifest..."
cd "$PROJECT_DIR"
uv run python3 "$SCRIPT_DIR/validate-manifest.py" > "$ARTIFACTS_DIR/manifest-validation.txt" 2>&1 || true

log "Evidence captured at $ARTIFACTS_DIR"
ls -la "$ARTIFACTS_DIR"
