from __future__ import annotations

from enum import Enum


class RuntimeStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"
    STOPPED = "stopped"
