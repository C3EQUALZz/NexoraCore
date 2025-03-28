from abc import ABC

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.services.user import UserClientService
from app.infrastructure.uow.teams.base import TeamsUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class TeamMembersEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: TeamsUnitOfWork, broker: BaseMessageBroker) -> None:
        self._uow: TeamsUnitOfWork = uow
        self._broker: BaseMessageBroker = broker


class TeamMembersCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: TeamsUnitOfWork, service: UserClientService) -> None:
        self._uow: TeamsUnitOfWork = uow
        self._service: UserClientService = service
