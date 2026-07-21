from dataclasses import dataclass


@dataclass
class RequestContext:
    request_id: str
    correlation_id: str
