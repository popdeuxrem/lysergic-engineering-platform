# Development Environment Runbook

## Requirements

- Python 3.12+
- uv
- Node.js 22+
- pnpm
- Docker

## Environment Setup

Create a local `.env` file from the example:

```sh
cp .env.example .env
```

The `.env` file is gitignored and is only used for local runtime configuration.

## Start Runtime

```sh
docker compose up
```

## Validate Services

### API

```sh
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/version
curl http://localhost:8000/api/v1/health
```

### Operations Console

```sh
curl http://localhost:3000
```

### Dependencies

```sh
docker compose exec postgres pg_isready
docker compose exec redis redis-cli ping
```

## Validate M0.5 Runtime

```sh
docker compose config
docker compose build
docker compose up -d
docker compose ps
curl http://localhost:8000/health
curl http://localhost:3000
docker compose exec postgres pg_isready
docker compose exec redis redis-cli ping
```

Evidence artifacts are captured in `docs/validation/artifacts/M0.5/`.

## CI Validation

The repository includes a GitHub Actions workflow at `.github/workflows/validation.yml`.

Workflow triggers:

- `push` to `main`
- `pull_request` to `main`

Jobs:

- `backend` — uv sync, pytest, ruff, mypy
- `frontend` — pnpm install, lint, typecheck, test, build
- `docker-compose` — compose config, build, up, health checks, down

Evidence artifacts are captured in `docs/validation/artifacts/M0.6/`.
