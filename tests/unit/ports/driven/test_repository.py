import dataclasses
import uuid
from abc import ABC, abstractmethod
from typing import Any

import pytest

from crypkit.core.error import DuplicityError, NotFoundError
from crypkit.core.model import CryptoCurrency, CryptoId, Symbol
from crypkit.ports.driven.repository import Repository


@dataclasses.dataclass
class Inserted:
    id_: uuid.UUID
    symbol: str
    metadata: dict[str, Any]


class RepositoryTest(ABC):
    """Abstract test suite for all Repository implementations."""

    @abstractmethod
    @pytest.fixture
    async def repository(self) -> Repository:
        """Fixture providing a concrete implementation of Repository."""

    @abstractmethod
    async def empty(self) -> None:
        """Empty the repository."""

    @abstractmethod
    async def insert(self, row: dict[str, Any]) -> None:
        """Insert one row into the repository."""

    @abstractmethod
    async def load_by_id(self, id_: uuid.UUID) -> tuple[uuid.UUID, str, dict[str, Any]]:
        """Load one record from the repository."""

    @abstractmethod
    async def load_all(self) -> list[tuple[uuid.UUID, str, dict[str, Any]]]:
        """Load all records from the repository."""

    @pytest.fixture(autouse=True)
    async def setup_before_each_test(self, repository: Repository) -> None:
        await self.empty()

    async def test_load_all_empty(self, repository: Repository) -> None:
        # given empty repository
        # when load_all is called
        it = await repository.load_all()

        # then it returns one Cryptocurrency
        assert it == []

    async def test_load_one(self, repository: Repository) -> None:
        # given one cryptocurrency in repository
        inserted = await self._insert()

        # when load_all is called
        it = await repository.load_all()

        # then it returns one CryptoCurrency
        assert it == [
            CryptoCurrency(
                id_=CryptoId(inserted.id_),
                symbol=Symbol(inserted.symbol),
                metadata=inserted.metadata,
            )
        ]

    async def test_load_multiple(self, repository: Repository) -> None:
        # given many cryptocurrencies in repository
        expected: list[Inserted] = []
        for i in range(10):
            inserted = await self._insert(
                symbol=f"symbol{i}",
                metadata={"symbol": f"symbol{i}", "other": ["funny", "data"], "i": i},
            )
            expected.append(inserted)

        # when load_all is called
        it = await repository.load_all()

        # then it returns all CryptoCurrencies sorted by id
        expected = sorted(expected, key=lambda x: x.id_)
        assert it == [
            CryptoCurrency(
                id_=CryptoId(i.id_),
                symbol=Symbol(i.symbol),
                metadata=i.metadata,
            )
            for i in expected
        ]

    async def test_delete_empty(self, repository: Repository) -> None:
        with pytest.raises(NotFoundError) as context:
            # given empty repository
            # when delete is called
            await repository.delete(CryptoId(id_=uuid.uuid4()))

        # then exception is raised
        assert context.type == NotFoundError

    async def test_delete_not_found(self, repository: Repository) -> None:
        with pytest.raises(NotFoundError) as context:
            # given one CryptoCurrency in repository
            inserted = await self._insert()

            # when delete is called with different id
            await repository.delete(CryptoId(id_=uuid.uuid4()))

        # then exception is raised
        assert context.type == NotFoundError
        # and CryptoCurrency is still there
        it = await self.load_by_id(id_=inserted.id_)
        assert it == (inserted.id_, inserted.symbol, inserted.metadata)

    async def test_delete_found(self, repository: Repository) -> None:
        # given many cryptocurrencies in repository
        inserted = []
        for i in range(10):
            insert = await self._insert(
                symbol=f"symbol{i}",
                metadata={"symbol": f"symbol{i}", "other": ["funny", "data"], "i": i},
            )
            inserted.append(insert)

        # when delete is called with first id
        await repository.delete(CryptoId(id_=inserted[0].id_))

        # then the one is removed from repository
        all_in_repo = await self.load_all()
        assert len(all_in_repo) == len(inserted) - 1
        for one_in_repo in all_in_repo:
            assert one_in_repo[0] != inserted[0].id_

    async def test_save_duplicate(self, repository: Repository) -> None:
        with pytest.raises(DuplicityError) as context:
            # given one cryptocurrency in repository
            inserted = await self._insert()

            # when save is called with the same id
            await repository.save(
                CryptoCurrency(
                    id_=CryptoId(inserted.id_), symbol=Symbol("anything"), metadata={}
                )
            )

        # then the exception is raised
        assert context.type == DuplicityError

    async def test_save(self, repository: Repository) -> None:
        # given empty repository
        id_ = uuid.uuid4()
        symbol = "anything"
        metadata = {"symbol": symbol}
        expected = CryptoCurrency(
            id_=CryptoId(id_), symbol=Symbol(symbol), metadata=metadata
        )

        # when save is called
        it = await repository.save(expected)

        # then cryptocurrency is saved in repository
        all_in_repo = await self.load_all()
        assert len(all_in_repo) == 1
        the_one = all_in_repo[0]
        assert the_one[0] == id_
        assert the_one[1] == symbol
        assert the_one[2] == metadata

        # and it is returned
        assert expected == it

    async def test_update_not_found(self, repository: Repository) -> None:
        with pytest.raises(NotFoundError) as context:
            # given one CryptoCurrency in repository
            await self._insert()

            # when update is called with different id
            await repository.update(
                CryptoCurrency(
                    id_=CryptoId(uuid.uuid4()), symbol=Symbol("anything"), metadata={}
                )
            )

        # then exception is raised
        assert context.type == NotFoundError

    async def test_update(self, repository: Repository) -> None:
        # given two CryptoCurrencies in repository
        inserted = await self._insert()
        await self._insert()

        # when update is called with the same id and different symbol
        update_symbol = "anything"
        update_metadata = {"symbol": update_symbol}
        it = await repository.update(
            CryptoCurrency(
                id_=CryptoId(inserted.id_),
                symbol=Symbol(update_symbol),
                metadata=update_metadata,
            )
        )

        # then it is updated
        all_in_repo = await self.load_all()
        assert len(all_in_repo) == 2
        the_one = next(filter(lambda x: x[0] == inserted.id_, all_in_repo))
        assert the_one[0] == inserted.id_
        assert the_one[1] == update_symbol
        assert the_one[2] == update_metadata
        # and updated value is returned
        assert it == CryptoCurrency(
            id_=CryptoId(inserted.id_),
            symbol=Symbol(update_symbol),
            metadata=update_metadata,
        )

    async def _insert(
        self, symbol: str = "symbol", metadata: dict[str, Any] | None = None
    ) -> Inserted:
        a_symbol = symbol or "symbol"
        a_metadata = metadata or {
            "symbol": symbol or "symbol",
            "other": ["funny", "data"],
        }
        id_ = uuid.uuid4()
        await self.insert(
            row={
                "id": id_,
                "symbol": a_symbol,
                "metadata": a_metadata,
            }
        )
        return Inserted(id_, a_symbol, a_metadata)
