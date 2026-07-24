from runtime.configuration.exceptions import (
    MergeConflictError,
    ProfileNotFoundError,
    ProviderNotFoundError,
)


def test_provider_not_found() -> None:
    try:
        raise ProviderNotFoundError("missing")
    except ProviderNotFoundError as e:
        assert e.provider_id == "missing"
        assert "missing" in str(e)


def test_profile_not_found() -> None:
    try:
        raise ProfileNotFoundError("missing")
    except ProfileNotFoundError as e:
        assert e.profile_id == "missing"


def test_merge_conflict() -> None:
    try:
        raise MergeConflictError("key", "a", "b")
    except MergeConflictError as e:
        assert e.key == "key"
        assert e.left == "a"
        assert e.right == "b"
