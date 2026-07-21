from src.api.v1.schemas.common import ServiceInfo


class HealthResponse(ServiceInfo):
    status: str


class VersionResponse(ServiceInfo):
    environment: str
