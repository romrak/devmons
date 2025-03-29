import uuid
from unittest.mock import AsyncMock

from crypkit.core.model import CryptoCurrency, CryptoId, Symbol
from crypkit.service.crypto import CryptoService


async def test_reads_from_repository_using_unit_of_work(
    crypto_service: CryptoService, unit_of_work: AsyncMock, repository: AsyncMock
) -> None:
    # given nothing special

    # when read is called
    await crypto_service.read()

    # then assert repository is called inside a unit of work context
    unit_of_work.__aenter__.assert_called_once()
    unit_of_work.__aexit__.assert_called_once()
    repository.load_all.assert_called_once()


async def test_returns_what_is_in_repository(crypto_service: CryptoService, repository: AsyncMock) -> None:
    # given there are some CryptoCurrencies in Repository
    crypto_currencies = [
        CryptoCurrency(id_=CryptoId(uuid.uuid4()), symbol=Symbol(f"symbol{i}"), metadata={}) for i in range(5)
    ]
    repository.load_all.return_value = crypto_currencies

    # when read is called
    it = await crypto_service.read()

    # it returns the same cryptocurrencies
    assert it == crypto_currencies
