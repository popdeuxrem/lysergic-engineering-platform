from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ValueObject:
    """Base class for domain value objects.

    Value objects are immutable, compared by structural equality,
    and carry no identity.
    """
