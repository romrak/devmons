from unittest.mock import AsyncMock

import pytest

from crypkit.ports.driven.coingecko import CoinGecko
from crypkit.ports.driven.repository import Repository, UnitOfWork
from crypkit.service.crypto import CryptoService


@pytest.fixture()
def repository() -> Repository:
    return AsyncMock(spec=Repository)


@pytest.fixture()
def unit_of_work(repository: Repository) -> UnitOfWork:
    mock = AsyncMock(spec=UnitOfWork)
    mock.__aenter__.return_value = repository
    mock.__aexit__.return_value = None
    return mock


@pytest.fixture()
def coin_gecko() -> CoinGecko:
    return AsyncMock(spec=CoinGecko)

@pytest.fixture()
def crypto_service(unit_of_work: UnitOfWork, coin_gecko: CoinGecko) -> CryptoService:
    return CryptoService(unit_of_work=unit_of_work, coin_gecko=coin_gecko)
