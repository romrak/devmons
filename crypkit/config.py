from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from crypkit.adapters.driven.repository.config import PostgresSettings


class Config(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    coin_gecko_api_key: str
    cache_expiration_seconds: int = Field(ge=1)

    model_config = SettingsConfigDict(env_prefix="CRYPKIT_")
