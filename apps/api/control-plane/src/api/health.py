from fastapi import APIRouter

from src.config.settings import get_settings

router = APIRouter()

@router.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()

    return {
        "service": settings.service_name,
        "status": "healthy",
        "version": settings.version,
    }

@router.get("/version")
def version() -> dict[str, str]:
    settings = get_settings()

    return {
        "service": settings.service_name,
        "version": settings.version,
        "environment": settings.environment,
    }
