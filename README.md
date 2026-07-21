# Lysergic Engineering Platform (LEP)

LEP is a governed engineering intelligence platform designed to coordinate engineering workflows, preserve evidence, and provide controlled intelligence-assisted engineering capabilities.

## Repository Structure

- `apps/` application services
- `services/` domain services
- `packages/` shared libraries and contracts
- `database/` migrations and seeds
- `infrastructure/` deployment definitions
- `docs/` architecture and operational documentation

## M0 Repository Foundation

The initial milestone establishes:

- repository topology
- development tooling
- runtime foundation
- validation framework
- shared contracts boundary

Excluded from M0:

- autonomous agents
- intelligence orchestration
- workflow execution
- production mutation

## Development

### Start runtime

```sh
docker compose up
Validate repository
make validate
