from typing import Self

from app.infrastructure.repositories.users.alchemy import SQLAlchemyUsersRepository
from app.infrastructure.repositories.users.base import UsersRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork


class SQLAlchemyTradingResultUnitOfWork(SQLAlchemyAbstractUnitOfWork, UsersUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users: UsersRepository = SQLAlchemyUsersRepository(session=self._session)
        return uow
