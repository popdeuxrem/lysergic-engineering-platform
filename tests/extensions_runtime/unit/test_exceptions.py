from runtime.extensions.exceptions import (
    ExtensionRuntimeConflictError,
    ExtensionRuntimeNotFoundError,
    InvalidLifecycleTransitionError,
)


def test_not_found() -> None:
    e = ExtensionRuntimeNotFoundError("ext-1")
    assert e.extension_id == "ext-1"


def test_conflict() -> None:
    e = ExtensionRuntimeConflictError("ext-1")
    assert e.extension_id == "ext-1"


def test_invalid_transition() -> None:
    e = InvalidLifecycleTransitionError("installed", "loaded")
    assert "installed" in str(e)
