from runtime.configuration.profile import ProfileDefinition, ProfileManager


def test_define() -> None:
    m = ProfileManager()
    m.define(ProfileDefinition(profile_id="dev", name="Development"))
    assert "dev" in m


def test_define_duplicate_raises() -> None:
    m = ProfileManager()
    m.define(ProfileDefinition(profile_id="dev", name="Dev"))
    try:
        m.define(ProfileDefinition(profile_id="dev", name="Dev 2"))
        assert False
    except ValueError:
        pass


def test_activate() -> None:
    m = ProfileManager()
    m.define(ProfileDefinition(profile_id="prod", name="Production", config={"db.host": "prod-db"}))
    m.activate("prod")
    assert m.active == "prod"


def test_activate_missing_raises() -> None:
    m = ProfileManager()
    try:
        m.activate("missing")
        assert False
    except Exception:  # noqa: BLE001, S110
        pass


def test_get() -> None:
    m = ProfileManager()
    p = ProfileDefinition(profile_id="test", name="Test")
    m.define(p)
    assert m.get("test") is p
    assert m.get("missing") is None


def test_delete() -> None:
    m = ProfileManager()
    m.define(ProfileDefinition(profile_id="tmp", name="Temp"))
    assert m.delete("tmp") is True
    assert "tmp" not in m


def test_resolved_config_no_active() -> None:
    m = ProfileManager()
    assert m.resolved_config() == {}


def test_resolved_config_single() -> None:
    m = ProfileManager()
    m.define(ProfileDefinition(profile_id="dev", name="Dev", config={"key": "val"}))
    m.activate("dev")
    assert m.resolved_config() == {"key": "val"}


def test_resolved_config_with_parent() -> None:
    m = ProfileManager()
    m.define(ProfileDefinition(profile_id="base", name="Base", config={"a": "base", "b": "base"}))
    m.define(ProfileDefinition(profile_id="child", name="Child", parent="base", config={"b": "child", "c": "child"}))
    m.activate("child")
    config = m.resolved_config()
    assert config["a"] == "base"
    assert config["b"] == "child"
    assert config["c"] == "child"


def test_delete_active_clears() -> None:
    m = ProfileManager()
    m.define(ProfileDefinition(profile_id="act", name="Active"))
    m.activate("act")
    m.delete("act")
    assert m.active is None


def test_count() -> None:
    m = ProfileManager()
    assert m.count == 0
    m.define(ProfileDefinition(profile_id="a", name="A"))
    assert m.count == 1
