from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    service_name: str = "lep-control-plane"
    version: str = "0.1.0"
    environment: str = "development"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
