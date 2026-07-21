from fastapi import APIRouter

from src.api.v1.routers.health import router as v1_health_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(v1_health_router)
