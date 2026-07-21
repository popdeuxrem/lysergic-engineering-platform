import os

from src.config.settings import Settings, get_settings


def test_database_configuration_loaded() -> None:
    settings = Settings(
        postgres_host="db.example.com",
        postgres_port=5433,
        postgres_db="testdb",
        postgres_user="testuser",
        postgres_password="testpass",
    )

    assert settings.postgres_host == "db.example.com"
    assert settings.postgres_port == 5433
    assert settings.postgres_db == "testdb"
    assert settings.postgres_user == "testuser"
    assert settings.postgres_password == "testpass"


def test_database_configuration_defaults() -> None:
    settings = Settings()

    assert settings.postgres_host == "localhost"
    assert settings.postgres_port == 5432
    assert settings.postgres_db == "lep"
    assert settings.postgres_user == "lep"
    assert settings.postgres_password == "lep"


def test_database_configuration_from_environment() -> None:
    env_vars = {
        "POSTGRES_HOST": "env.example.com",
        "POSTGRES_PORT": "6432",
        "POSTGRES_DB": "envdb",
        "POSTGRES_USER": "envuser",
        "POSTGRES_PASSWORD": "envpass",
    }

    for key, value in env_vars.items():
        os.environ[key] = value

    try:
        settings = Settings()

        assert settings.postgres_host == "env.example.com"
        assert settings.postgres_port == 6432
        assert settings.postgres_db == "envdb"
        assert settings.postgres_user == "envuser"
        assert settings.postgres_password == "envpass"
    finally:
        for key in env_vars:
            os.environ.pop(key, None)
            get_settings.cache_clear()
