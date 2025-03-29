import uuid
from unittest.mock import AsyncMock

from crypkit.core.model import CryptoId
from crypkit.service.crypto import CryptoService


async def test_deletes_from_repository_using_unit_of_work(
    crypto_service: CryptoService, unit_of_work: AsyncMock, repository: AsyncMock
) -> None:
    # given id of cryptocurrency
    id_ = uuid.uuid4()

    # when delete is called with id
    await crypto_service.delete(id_=id_)

    # then repository delete is called using unit of work with CryptoId
    unit_of_work.__aenter__.assert_called_once()
    unit_of_work.__aexit__.assert_called_once()
    repository.delete.assert_called_once_with(CryptoId(id_))
