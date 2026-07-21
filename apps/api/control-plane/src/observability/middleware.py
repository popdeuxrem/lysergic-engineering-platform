import logging
import time
from uuid import uuid4

from fastapi import Request, Response

from src.observability.context import RequestContext

logger = logging.getLogger("lep.observability.middleware")

CORRELATION_ID_HEADER = "X-Correlation-ID"
REQUEST_ID_HEADER = "X-Request-ID"


def extract_request_context(request: Request) -> RequestContext:
    request_id = str(uuid4())
    correlation_id = request.headers.get(CORRELATION_ID_HEADER, str(uuid4()))
    return RequestContext(request_id=request_id, correlation_id=correlation_id)


async def request_context_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
    ctx = extract_request_context(request)
    request.state.request_id = ctx.request_id
    request.state.correlation_id = ctx.correlation_id

    logger.info(
        "request.started",
        extra={
            "request_id": ctx.request_id,
            "correlation_id": ctx.correlation_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    start = time.monotonic()
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.error(
            "request.failed",
            extra={
                "request_id": ctx.request_id,
                "correlation_id": ctx.correlation_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms,
            },
        )
        raise

    duration_ms = int((time.monotonic() - start) * 1000)

    response.headers[REQUEST_ID_HEADER] = ctx.request_id
    response.headers[CORRELATION_ID_HEADER] = ctx.correlation_id

    logger.info(
        "request.completed",
        extra={
            "request_id": ctx.request_id,
            "correlation_id": ctx.correlation_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )

    return response
