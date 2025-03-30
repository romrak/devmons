from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from crypkit.core.model import CryptoCurrencyMemento


class CryptoCurrencyResponse(BaseModel):
    id: UUID
    symbol: str
    metadata: dict[str, Any]

    @classmethod
    def from_memento(cls, memento: CryptoCurrencyMemento) -> "CryptoCurrencyResponse":
        return cls(
            id=UUID(memento.id_), symbol=memento.symbol, metadata=memento.metadata
        )


class CreateRequest(BaseModel):
    id: UUID
    symbol: str = Field(min_length=1)


class UpdateRequest(BaseModel):
    symbol: str = Field(min_length=1)
