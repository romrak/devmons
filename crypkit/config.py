from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from crypkit.adapters.driven.repository.config import PostgresSettings


class RedisSettings(BaseSettings):
    host: str
    port: int = 6379
    db: int = 0
    cache_expiration_seconds: int = Field(ge=1)
    model_config = SettingsConfigDict(env_prefix="CRYPKIT_REDIS_")


class Config(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    coin_gecko_api_key: str

    model_config = SettingsConfigDict(env_prefix="CRYPKIT_")
