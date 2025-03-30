import uuid
from unittest.mock import AsyncMock

import pytest

from crypkit.core.error import (
    CoingeckoNotFoundError,
    CoingeckoNotWorkingError,
    NotFoundError,
)
from crypkit.core.model import CryptoCurrency, CryptoId, Symbol
from crypkit.ports.driving.crud import UpdateDTO
from crypkit.service.crypto import CryptoService

update_request = UpdateDTO(id=uuid.uuid4(), symbol="something")


async def test_not_found_in_coin_gecko(
    crypto_service: CryptoService, coin_gecko: AsyncMock, repository: AsyncMock
) -> None:
    with pytest.raises(CoingeckoNotFoundError) as context:
        # given update request
        # when it's symbol doesn't exist in coin gecko
        coin_gecko.symbol_info.side_effect = CoingeckoNotFoundError()
        # and we call update with it
        await crypto_service.update(update_request)

        # then cryptocurrency is not updated in repository
        repository.update.assert_not_called()
    # and we raised exception
    assert context.type == CoingeckoNotFoundError


async def test_coin_gecko_not_working(
    crypto_service: CryptoService, coin_gecko: AsyncMock, repository: AsyncMock
) -> None:
    with pytest.raises(CoingeckoNotWorkingError) as context:
        # given update request
        # when coin gecko is not working
        coin_gecko.symbol_info.side_effect = CoingeckoNotWorkingError()
        # and we call update with it
        await crypto_service.update(update_request)

        # then cryptocurrency is not updated in repository
        repository.update.assert_not_called()
    # and we raised exception
    assert context.type == CoingeckoNotWorkingError


async def test_coin_gecko_working_but_dont_exist(
    crypto_service: CryptoService,
    coin_gecko: AsyncMock,
    repository: AsyncMock,
    unit_of_work: AsyncMock,
) -> None:
    with pytest.raises(NotFoundError) as context:
        # given There is a symbol with data in coin gecko
        # but There is not cryptocurrency in repository
        repository.update.side_effect = NotFoundError

        # when we call update with the symbol
        await crypto_service.update(update_request)

    # then Exception is raised
    assert context.type == NotFoundError


async def test_coin_gecko_working(
    crypto_service: CryptoService,
    coin_gecko: AsyncMock,
    repository: AsyncMock,
    unit_of_work: AsyncMock,
) -> None:
    # given There is a symbol with data in coin gecko
    symbol = update_request.symbol
    data = {
        "some": "data",
        "for": ["this", "symbol"],
    }
    expected = CryptoCurrency(
        id_=CryptoId(update_request.id), symbol=Symbol(symbol), metadata=data
    )
    repository.update.return_value = expected

    # when we call update with the symbol
    it = await crypto_service.update(update_request)

    # then we update the cryptocurrency in repository using unit of work
    unit_of_work.__aenter__.assert_called_once()
    unit_of_work.__aexit__.assert_called_once()
    repository.update.assert_called_once_with(expected)
    # and return it
    assert it == expected
