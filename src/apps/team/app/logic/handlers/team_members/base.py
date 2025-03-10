from abc import ABC

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

    def __init__(self, uow: TeamsUnitOfWork) -> None:
        self._uow: TeamsUnitOfWork = uow


class TeamMembersCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: TeamsUnitOfWork) -> None:
        self._uow: TeamsUnitOfWork = uow
