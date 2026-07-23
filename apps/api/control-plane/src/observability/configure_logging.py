import json
import logging
import sys
from datetime import UTC, datetime

from src.config.settings import Settings


class JsonFormatter(logging.Formatter):
    def __init__(self, service_name: str, version: str) -> None:
        super().__init__()
        self.service_name = service_name
        self.version = version

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "service": self.service_name,
            "version": self.version,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for key in ("request_id", "correlation_id", "method", "path", "status_code", "duration_ms"):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value

        return json.dumps(payload)

def configure_logging(settings: Settings) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        JsonFormatter(
            service_name=settings.service_name,
            version=settings.version,
        )
    )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
