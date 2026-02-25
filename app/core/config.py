from __future__ import annotations

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = Field(default="dev", alias="APP_ENV")
    app_name: str = Field(default="PingSA", alias="APP_NAME")
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@postgres:5432/pingsa", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    webhook_verify_token: str = Field(default="verify-me", alias="WHATSAPP_VERIFY_TOKEN")
    whatsapp_token: str = Field(default="", alias="WHATSAPP_TOKEN")
    whatsapp_phone_number_id: str = Field(default="", alias="WHATSAPP_PHONE_NUMBER_ID")
    whatsapp_business_account_id: str = Field(default="", alias="WHATSAPP_BUSINESS_ACCOUNT_ID")
    admin_api_key: str = Field(default="changeme", alias="ADMIN_API_KEY")
    data_encryption_key: str = Field(alias="DATA_ENCRYPTION_KEY")
    cors_origins: list[str] = Field(default_factory=list, alias="CORS_ORIGINS")
    rate_limit_per_minute: int = Field(default=10, alias="RATE_LIMIT_PER_MINUTE")
    consent_version: str = Field(default="v1", alias="CONSENT_VERSION")
    safety_ping_minutes_before: int = Field(default=5, alias="SAFETY_PING_MINUTES_BEFORE")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
