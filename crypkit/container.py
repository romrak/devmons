import httpx
import redis.asyncio as redis
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from crypkit.adapters.driven.coingecko import CachedCoinGecko
from crypkit.adapters.driven.repository.config import PostgresSettings
from crypkit.adapters.driven.repository.sqlalchemy import SqlAlchemyUnitOfWork
from crypkit.service.crypto import CryptoService


class CrypkitContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["crypkit.adapters.api.crypto"]
    )

    config = providers.Configuration()
    postgres_settings = providers.Singleton(PostgresSettings)

    redis_client = providers.Singleton(redis.Redis, host="localhost", port=6379, db=0)
    httpx_client = providers.Singleton(httpx.AsyncClient)

    engine = providers.Singleton(create_async_engine, url=postgres_settings().to_url())
    session_factory = providers.Singleton(
        async_sessionmaker, bind=engine, expire_on_commit=False
    )

    unit_of_work = providers.Singleton(
        SqlAlchemyUnitOfWork, session_factory=session_factory
    )

    coin_gecko = providers.Singleton(
        CachedCoinGecko,
        redis_client=redis_client,
        httpx_client=httpx_client,
        api_key=config.coin_gecko_api_key,
        cache_expiration_seconds=config.cache_expiration_seconds,
    )

    crypto_service = providers.Singleton(
        CryptoService, unit_of_work=unit_of_work, coin_gecko=coin_gecko
    )
