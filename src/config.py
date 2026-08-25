"""Validated configuration for the Core IA HTTP service."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    """Service settings loaded from environment variables and ``.env``."""

    service_name: str = Field(min_length=1, max_length=100)
    environment: Literal["development", "test", "production"]

    model_config = SettingsConfigDict(
        env_file=PROJECT_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        strict=True,
    )

    @field_validator("service_name")
    @classmethod
    def service_name_must_contain_non_whitespace(cls, value: str) -> str:
        """Normalize valid names and reject values that contain only whitespace."""

        normalized = value.strip()
        if not normalized:
            raise ValueError("service_name must contain non-whitespace characters")
        return normalized


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide validated service configuration."""

    return Settings(_env_file=PROJECT_ENV_FILE)


def reset_settings_cache() -> None:
    """Clear cached settings for controlled lifecycle tests."""

    get_settings.cache_clear()


def create_model(*_: object, **__: object) -> object:
    """Reject use of the retired POC provider construction path.

    This compatibility symbol lets unmodified migration-input modules import
    without introducing a Gemini dependency into the Core IA service lifecycle.
    """

    raise RuntimeError(
        "The legacy POC model factory is retired; use the Core IA HTTP service."
    )
