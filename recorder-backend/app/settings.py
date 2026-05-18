from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    yle_client_id: str | None = None
    yle_client_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
