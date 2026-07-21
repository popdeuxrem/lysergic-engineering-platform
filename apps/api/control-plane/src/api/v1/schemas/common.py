from pydantic import BaseModel

from src.api.errors import ErrorDetail


class ErrorResponse(BaseModel):
    error: ErrorDetail


class ServiceInfo(BaseModel):
    service: str
    version: str
