from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    Values can be overridden by environment variables or .env file.
    """
    app_name: str = "Tazkiya API"
    debug:bool = True
    database_url: str = "sqlite:///./tazkiya.db"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    lru_cache ensures we only create Settings once (singleton).
    """
    return Settings()
    