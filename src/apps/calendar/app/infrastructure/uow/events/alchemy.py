from typing import Self

from app.infrastructure.repositories.meetings.alchemy import SQLAlchemyMeetingsRepository
from app.infrastructure.repositories.tasks.alchemy import SQLAlchemyTasksRepository
from app.infrastructure.repositories.meetings.base import MeetingsRepository
from app.infrastructure.repositories.tasks.base import TasksRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.events.base import EventsUnitOfWork


class SQLAlchemyEventsUnitOfWork(SQLAlchemyAbstractUnitOfWork, EventsUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.tasks: TasksRepository = SQLAlchemyTasksRepository(session=self._session)
        self.meetings: MeetingsRepository = SQLAlchemyMeetingsRepository(session=self._session)
        return uow
