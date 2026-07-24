from runtime.assets.exceptions import (
    AssetConflictError,
    AssetNotFoundError,
    DependencyCycleError,
    InvalidLifecycleTransitionError,
)


def test_asset_not_found() -> None:
    e = AssetNotFoundError("ast-1")
    assert e.asset_id == "ast-1"
    assert "ast-1" in str(e)


def test_asset_conflict() -> None:
    e = AssetConflictError("ast-1")
    assert e.asset_id == "ast-1"


def test_dependency_cycle() -> None:
    e = DependencyCycleError("ast-1")
    assert e.node == "ast-1"


def test_invalid_lifecycle_transition() -> None:
    e = InvalidLifecycleTransitionError("available", "registered")
    assert e.current == "available"
    assert e.target == "registered"
