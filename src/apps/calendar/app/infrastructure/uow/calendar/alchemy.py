from typing import Self

from app.infrastructure.repositories.calendar.alchemy import SQLAlchemyCalendarsRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.calendar.base import CalendarUnitOfWork


class SQLAlchemyCalendarUnitOfWork(SQLAlchemyAbstractUnitOfWork, CalendarUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.calendar = SQLAlchemyCalendarsRepository(session=self._session)
        return uow
