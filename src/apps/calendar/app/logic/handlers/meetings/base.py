from abc import ABC
from typing import override

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.uow.events.base import EventsUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class MeetingsEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    @override
    def __init__(self, uow: EventsUnitOfWork, broker: BaseMessageBroker) -> None:
        self._uow: EventsUnitOfWork = uow
        self._broker: BaseMessageBroker = broker


class MeetingsCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    @override
    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow: EventsUnitOfWork = uow
