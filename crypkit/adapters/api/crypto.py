from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from crypkit.adapters.api.schema import (
    CreateRequest,
    CryptoCurrencyResponse,
    UpdateRequest,
)
from crypkit.container import CrypkitContainer
from crypkit.core.error import (
    CoingeckoNotFoundError,
    CoingeckoNotWorkingError,
    DuplicityError,
    NotFoundError,
)
from crypkit.ports.driving.crud import CreateDTO, CrudOperations, UpdateDTO

router = APIRouter()


@router.post("/cryptocurrencies/", response_model=CryptoCurrencyResponse)
@inject
async def create_crypto(
    request: CreateRequest,
    crud_operations: Annotated[
        CrudOperations, Depends(Provide[CrypkitContainer.crud_operations])
    ],
) -> CryptoCurrencyResponse:
    try:
        value = await crud_operations.create(
            CreateDTO(id=request.id, symbol=request.symbol)
        )
        return CryptoCurrencyResponse.from_memento(value.memento())
    except CoingeckoNotFoundError:
        raise HTTPException(
            status_code=404, detail="CryptoCurrency not found in Coin Gecko"
        )
    except CoingeckoNotWorkingError:
        raise HTTPException(status_code=503, detail="Coingecko service is down")
    except DuplicityError:
        raise HTTPException(status_code=400, detail="CryptoCurrency already exists")


@router.get("/cryptocurrencies/", response_model=list[CryptoCurrencyResponse])
@inject
async def list_cryptocurrencies(
    crud_operations: Annotated[
        CrudOperations, Depends(Provide[CrypkitContainer.crud_operations])
    ],
) -> list[CryptoCurrencyResponse]:
    values = await crud_operations.read()
    return [CryptoCurrencyResponse.from_memento(value.memento()) for value in values]


@router.put("/cryptocurrencies/{uuid}", response_model=CryptoCurrencyResponse)
@inject
async def update_crypto(
    uuid: UUID,
    request: UpdateRequest,
    crud_operations: Annotated[
        CrudOperations, Depends(Provide[CrypkitContainer.crud_operations])
    ],
) -> CryptoCurrencyResponse:
    try:
        value = await crud_operations.update(UpdateDTO(id=uuid, symbol=request.symbol))
        return CryptoCurrencyResponse.from_memento(value.memento())
    except CoingeckoNotFoundError:
        raise HTTPException(
            status_code=404, detail="CryptoCurrency not found in Coin Gecko"
        )
    except CoingeckoNotWorkingError:
        raise HTTPException(status_code=503, detail="Coingecko service is down")
    except NotFoundError:
        raise HTTPException(status_code=404, detail="CryptoCurrency not found")


@router.delete("/cryptocurrencies/{uuid}")
@inject
async def delete_crypto(
    uuid: UUID,
    crud_operations: Annotated[
        CrudOperations, Depends(Provide[CrypkitContainer.crud_operations])
    ],
) -> None:
    try:
        await crud_operations.delete(uuid)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="CryptoCurrency not found")
