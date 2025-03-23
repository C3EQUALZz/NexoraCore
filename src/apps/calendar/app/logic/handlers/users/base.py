from abc import ABC
from typing import override

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.uow.events.base import EventsUnitOfWork
from app.logic.handlers.base import AbstractEventHandler
from app.logic.types.handlers import ET


class UsersEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    @override
    def __init__(self, uow: EventsUnitOfWork, broker: BaseMessageBroker) -> None:
        self._uow: EventsUnitOfWork = uow
        self._broker: BaseMessageBroker = broker
