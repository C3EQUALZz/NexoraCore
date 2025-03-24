from abc import ABC

from app.infrastructure.repositories.meetings.base import MeetingsRepository
from app.infrastructure.repositories.tasks.base import TasksRepository
from app.infrastructure.repositories.users.base import UsersRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class EventsUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with events, that is used by service layer of events module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    tasks: TasksRepository
    meetings: MeetingsRepository
    users: UsersRepository
