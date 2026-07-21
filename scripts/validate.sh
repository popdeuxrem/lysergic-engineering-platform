#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../apps/api/control-plane" && pwd)"

log() {
    echo "[validate] $*"
}

fail() {
    echo "[validate] FAILED: $*"
    exit 1
}

log "Running validation in $PROJECT_DIR"

cd "$PROJECT_DIR"

log "uv sync..."
uv sync || fail "uv sync failed"

log "uv run pytest..."
uv run pytest || fail "pytest failed"

log "uv run ruff check ."
uv run ruff check . || fail "ruff failed"

log "uv run mypy src..."
uv run mypy src || fail "mypy failed"

log "docker build ..."
docker build . -t lep-control-plane:validate || fail "docker build failed"

log "All validation steps passed"
