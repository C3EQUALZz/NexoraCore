from abc import ABC

from app.logic.types.handlers import (
    CT,
    ET,
)
from app.infrastructure.uow.team_members.base import TeamMembersUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)


class TeamMembersEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: TeamMembersUnitOfWork) -> None:
        self._uow: TeamMembersUnitOfWork = uow


class TeamMembersCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: TeamMembersUnitOfWork) -> None:
        self._uow: TeamMembersUnitOfWork = uow
