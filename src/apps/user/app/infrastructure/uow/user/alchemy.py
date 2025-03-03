from typing import Self

from app.infrastructure.repositories.user.alchemy import SQLAlchemyUserRepository
from app.infrastructure.repositories.user.base import UserRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.user.base import UserUnitOfWork


class SQLAlchemyTradingResultUnitOfWork(SQLAlchemyAbstractUnitOfWork, UserUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.user: UserRepository = SQLAlchemyUserRepository(session=self._session)
        return uow
