from extensions.sdk.compatibility import CompatibilityChecker


def test_exact_match() -> None:
    c = CompatibilityChecker()
    compat, msg = c.check_sdk_compatibility("1.0.0")
    assert compat is True
    assert msg == ""


def test_extension_requires_newer_sdk() -> None:
    c = CompatibilityChecker()
    compat, msg = c.check_sdk_compatibility("2.0.0")
    assert compat is False
    assert "2.0.0" in msg


def test_extension_requires_older_sdk() -> None:
    c = CompatibilityChecker()
    compat, _ = c.check_sdk_compatibility("0.9.0")
    assert compat is True


def test_extension_with_max_sdk() -> None:
    c = CompatibilityChecker()
    compat, _ = c.check_sdk_compatibility("1.0.0", manifest_max_sdk="1.0.0")
    assert compat is True


def test_extension_exceeds_max_sdk() -> None:
    c = CompatibilityChecker()
    compat, _ = c.check_sdk_compatibility("0.5.0", manifest_max_sdk="0.9.0")
    assert compat is False


def test_dependency_compatibility() -> None:
    c = CompatibilityChecker()
    compat, _ = c.check_dependency_compatibility("2.0.0", "1.0.0")
    assert compat is True


def test_dependency_incompatible() -> None:
    c = CompatibilityChecker()
    compat, _ = c.check_dependency_compatibility("0.5.0", "1.0.0")
    assert compat is False


def test_parse_valid_version() -> None:
    c = CompatibilityChecker()
    result = c._parse("1.2.3")
    assert result == (1, 2, 3)


def test_parse_invalid_version() -> None:
    c = CompatibilityChecker()
    result = c._parse("invalid")
    assert result is None


def test_parse_partial_version() -> None:
    c = CompatibilityChecker()
    result = c._parse("1.2")
    assert result is None
