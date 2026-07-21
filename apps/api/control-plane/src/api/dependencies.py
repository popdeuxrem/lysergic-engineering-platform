from uuid import uuid4

from fastapi import Request


def request_context(request: Request) -> None:
    if not hasattr(request.state, "request_id"):
        request.state.request_id = str(uuid4())
    if not hasattr(request.state, "correlation_id"):
        request.state.correlation_id = request.headers.get("X-Correlation-ID", str(uuid4()))
