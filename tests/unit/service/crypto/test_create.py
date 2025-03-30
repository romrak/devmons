import uuid
from unittest.mock import AsyncMock

import pytest

from crypkit.core.error import CoingeckoNotFoundError, CoingeckoNotWorkingError
from crypkit.core.model import CryptoCurrency, CryptoId, Symbol
from crypkit.ports.driving.crud import CreateDTO
from crypkit.service.crypto import CryptoService

create_request = CreateDTO(id=uuid.uuid4(), symbol="something")


async def test_not_found_in_coin_gecko(
    crypto_service: CryptoService, coin_gecko: AsyncMock, repository: AsyncMock
) -> None:
    with pytest.raises(CoingeckoNotFoundError) as context:
        # given create request
        # when it's symbol doesn't exist in coin gecko
        coin_gecko.symbol_info.side_effect = CoingeckoNotFoundError()
        # and we call create with it
        await crypto_service.create(create_request)

        # then cryptocurrency is not saved into repository
        repository.save.assert_not_called()
    # and we raised exception
    assert context.type == CoingeckoNotFoundError


async def test_coin_gecko_not_working(
    crypto_service: CryptoService, coin_gecko: AsyncMock, repository: AsyncMock
) -> None:
    with pytest.raises(CoingeckoNotWorkingError) as context:
        # given create request
        # when coin gecko is not working
        coin_gecko.symbol_info.side_effect = CoingeckoNotWorkingError()
        # and we call create with it
        await crypto_service.create(create_request)

        # then cryptocurrency is not saved into repository
        repository.save.assert_not_called()
    # and we raised exception
    assert context.type == CoingeckoNotWorkingError


async def test_coin_gecko_working(
    crypto_service: CryptoService,
    coin_gecko: AsyncMock,
    repository: AsyncMock,
    unit_of_work: AsyncMock,
) -> None:
    # given There is a symbol with data in coin gecko
    symbol = create_request.symbol
    data = {
        "some": "data",
        "for": ["this", "symbol"],
    }
    expected = CryptoCurrency(
        id_=CryptoId(create_request.id), symbol=Symbol(symbol), metadata=data
    )
    repository.save.return_value = expected

    # when we call create with the symbol
    it = await crypto_service.create(create_request)

    # then we save new cryptocurrency to repository using unit of work
    unit_of_work.__aenter__.assert_called_once()
    unit_of_work.__aexit__.assert_called_once()
    repository.save.assert_called_once_with(expected)
    # and return it
    assert it == expected
