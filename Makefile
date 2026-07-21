.PHONY: validate backend frontend

validate:
	@echo "Running LEP validation pipeline"
	$(MAKE) backend
	$(MAKE) frontend

backend:
	@echo "Backend validation"
	cd apps/api/control-plane && uv run ruff check .
	cd apps/api/control-plane && uv run mypy src
	cd apps/api/control-plane && uv run pytest

frontend:
	@echo "Frontend validation"
	cd apps/web/operations-console && pnpm lint
	cd apps/web/operations-console && pnpm typecheck
	cd apps/web/operations-console && pnpm test
