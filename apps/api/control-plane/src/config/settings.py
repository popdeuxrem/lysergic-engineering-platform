from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    service_name: str = "lep-control-plane"
    version: str = "0.1.0"
    environment: str = "development"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "lep"
    postgres_user: str = "lep"
    postgres_password: str = "lep"

@lru_cache
def get_settings() -> Settings:
    return Settings()
