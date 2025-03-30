from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    """Initialize Postgres configuration."""

    host: str
    port: int = 5432
    username: str
    password: str
    database_name: str
    max_connections: int = 5
    model_config = SettingsConfigDict(env_prefix="CRYPKIT_POSTGRES_")

    def to_url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"
