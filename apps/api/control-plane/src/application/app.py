from fastapi import FastAPI

from src.api.health import router as health_router
from src.api.router import v1_router
from src.config.settings import get_settings
from src.observability.configure_logging import configure_logging

def create_app() -> FastAPI:
    settings = get_settings()

    configure_logging(settings)

    app = FastAPI(
        title="LEP Control Plane",
        version=settings.version,
    )

    @app.get("/")
    def root() -> dict[str, str]:
        return {
            "service": settings.service_name,
            "message": "LEP Control Plane",
        }

    app.include_router(health_router)
    app.include_router(v1_router)

    return app
