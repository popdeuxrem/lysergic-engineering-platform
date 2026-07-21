from src.infrastructure.database import (
    Base,
    SessionLocal,
    create_database_engine,
    database_session,
    get_engine,
)


def test_database_infrastructure_imports() -> None:
    assert Base is not None
    assert SessionLocal is not None
    assert create_database_engine is not None
    assert database_session is not None
    assert get_engine is not None


def test_declarative_base_contains_known_tables() -> None:
    assert "executions" in Base.metadata.tables


def test_database_engine_url_uses_settings() -> None:
    engine = create_database_engine()
    url = str(engine.url)

    assert url.startswith("postgresql+psycopg://")
    assert "localhost" in url
    assert "5432" in url
    assert "lep" in url


def test_get_engine_returns_engine() -> None:
    engine = get_engine()
    assert str(engine.url).startswith("postgresql+psycopg://")
