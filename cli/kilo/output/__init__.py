from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CLIError:
    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, "details": self.details}


EXIT_CODES: dict[str, int] = {
    "SUCCESS": 0,
    "GENERAL_ERROR": 1,
    "INVALID_INPUT": 2,
    "VALIDATION_ERROR": 3,
    "PERMISSION_DENIED": 4,
    "RUNTIME_UNAVAILABLE": 5,
}


def format_output(data: Any, error: CLIError | None = None, format: str = "text") -> str:
    if format == "json":
        return _format_json(data, error)
    return _format_text(data, error)


def _format_json(data: Any, error: CLIError | None = None) -> str:
    if error:
        return json.dumps({"status": "error", "error": error.to_dict()}, indent=2)
    return json.dumps({"status": "success", "data": data}, indent=2)


def _format_text(data: Any, error: CLIError | None = None) -> str:
    if error:
        return f"Error [{error.code}]: {error.message}"
    if data is None:
        return ""
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{key}:")
                for k, v in value.items():
                    lines.append(f"  {k}: {v}")
            elif isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)
    if isinstance(data, list):
        return "\n".join(str(item) for item in data)
    return str(data)


def detect_format() -> str:
    if not sys.stdout.isatty():
        return "json"
    return "text"
