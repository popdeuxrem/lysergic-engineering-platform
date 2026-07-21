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
