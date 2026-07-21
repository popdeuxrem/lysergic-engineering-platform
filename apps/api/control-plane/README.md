# LEP Control Plane

FastAPI control plane foundation for LEP Reference Platform v0.1.0.

## Scope

Included:

- FastAPI application factory
- router composition
- typed configuration
- structured logging
- health endpoints
- version endpoint

Excluded:

- persistence
- authentication
- authorization
- workflows
- agents
- event infrastructure

## Development

Install dependencies:

```bash
uv sync
Run:
uv run uvicorn src.main:app --reload
Validate:
uv run pytest
uv run ruff check .
uv run mypy src
Runtime Endpoints
	•	/
	•	/health
	•	/version
	•	/api/v1/health
