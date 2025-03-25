from abc import ABC
from typing import override

from app.infrastructure.services.calendar.base import CalendarService
from app.infrastructure.services.user.base import UserService
from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.uow.task.base import TasksUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)

from app.logic.types.handlers import (
    CT,
    ET,
)


class TasksEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    @override
    def __init__(self, uow: TasksUnitOfWork, broker: BaseMessageBroker) -> None:
        self._uow: TasksUnitOfWork = uow
        self._broker: BaseMessageBroker = broker


class TasksCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    @override
    def __init__(self, uow: TasksUnitOfWork, client_service: UserService, calendar_service: CalendarService) -> None:
        self._uow: TasksUnitOfWork = uow
        self._client_service: UserService = client_service
        self._calendar_service: CalendarService = calendar_service
