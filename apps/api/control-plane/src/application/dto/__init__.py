from dataclasses import dataclass


@dataclass(frozen=True)
class BaseDTO:
    """Base class for application data transfer objects."""


@dataclass(frozen=True)
class Command(BaseDTO):
    """Base class for commands (side-effect operations)."""


@dataclass(frozen=True)
class Query(BaseDTO):
    """Base class for queries (read-only operations)."""


@dataclass(frozen=True)
class Result(BaseDTO):
    """Base class for operation results."""
