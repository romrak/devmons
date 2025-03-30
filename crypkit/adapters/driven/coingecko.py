from dataclasses import dataclass
from typing import Any, cast

import ujson
from httpx import AsyncClient
from redis.asyncio import Redis

from crypkit.core.error import CoingeckoNotFoundError
from crypkit.core.model import Symbol
from crypkit.ports.driven.coingecko import CoinGecko


@dataclass(frozen=True)
class CacheValue:
    symbol: str
    data: dict[Any, Any]


class CachedCoinGecko(CoinGecko):
    def __init__(
        self,
        redis_client: Redis,
        httpx_client: AsyncClient,
        api_key: str,
        cache_expiration_seconds: int,
    ):
        self._redis = redis_client
        self._httpx = httpx_client
        self._api_key = api_key
        self._cache_expiration_seconds = cache_expiration_seconds

    async def symbol_info(self, symbol: Symbol) -> dict[Any, Any]:
        data = await self._read_from_redis(symbol)
        if data is None:
            values = await self._repopulate_cache()
            filtered = list(filter(lambda x: x.symbol == symbol.chars, values))
            if len(filtered) == 0:
                raise CoingeckoNotFoundError()
            return filtered[0].data
        return data

    async def refresh(self) -> None:
        await self._repopulate_cache()

    async def _read_from_redis(self, symbol: Symbol) -> dict[Any, Any] | None:
        value = await self._redis.get(symbol.chars)
        if value is None:
            return None
        return cast(dict[Any, Any], ujson.loads(value))

    async def _repopulate_cache(self) -> list[CacheValue]:
        values = await self._read_from_coin_gecko()
        await self._store_to_redis(values)
        return values

    async def _read_from_coin_gecko(self) -> list[CacheValue]:
        response = await self._httpx.get(
            url="https://api.coingecko.com/api/v3/coins/list",
            headers={"x-cg-demo-api-key": self._api_key},
        )
        values = []
        for coin in response.json():
            values.append(CacheValue(symbol=coin["symbol"], data=coin))
        return values

    async def _store_to_redis(self, values: list[CacheValue]) -> None:
        pipeline = self._redis.pipeline()
        for value in values:
            # noinspection PyAsyncCall
            pipeline.setex(
                name=value.symbol,
                time=self._cache_expiration_seconds,
                value=ujson.dumps(value.data),
            )
        await pipeline.execute()
