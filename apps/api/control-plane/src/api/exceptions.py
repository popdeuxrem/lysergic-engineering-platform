from uuid import uuid4

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.api.errors import ErrorDetail


def build_error_response(
    request: Request,
    code: str,
    message: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid4()))
    return JSONResponse(
        status_code=status_code,
        content={
            "error": ErrorDetail(
                code=code,
                message=message,
                request_id=request_id,
            ).model_dump(),
        },
    )
