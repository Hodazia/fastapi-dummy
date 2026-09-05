from functools import lru_cache

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"

    database_url: str
    secret_key: str = "CHANGE_THIS_IN_PRODUCTION________"

    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    cors_origins: str = "*"
    access_token_expire_minutes: int = 30
    sql_echo: bool = False

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def cors_origins_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if not self.is_production:
            return self

        if self.secret_key == "CHANGE_THIS_IN_PRODUCTION________":
            raise ValueError("Set a strong SECRET_KEY before running in production")

        if len(self.secret_key) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters in production")

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
