from fastapi import APIRouter

from src.api.v1.schemas.health import HealthResponse, VersionResponse
from src.config.settings import get_settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        service=settings.service_name,
        status="healthy",
        version=settings.version,
    )


@router.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    settings = get_settings()
    return VersionResponse(
        service=settings.service_name,
        version=settings.version,
        environment=settings.environment,
    )
