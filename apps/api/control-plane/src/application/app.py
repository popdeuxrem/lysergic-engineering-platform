from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.api.exceptions import build_error_response
from src.api.health import router as health_router
from src.api.router import v1_router
from src.config.settings import get_settings
from src.observability.configure_logging import configure_logging
from src.observability.middleware import request_context_middleware


def create_app() -> FastAPI:
    settings = get_settings()

    configure_logging(settings)

    app = FastAPI(
        title="LEP Control Plane",
        version=settings.version,
    )

    app.middleware("http")(request_context_middleware)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return build_error_response(
            request=request,
            code="HTTP_ERROR",
            message=exc.detail,
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return build_error_response(
            request=request,
            code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
