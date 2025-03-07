from abc import ABC

from app.infrastructure.repositories.team_members.base import TeamMembersRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class TeamMembersUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with teams, that is used by service layer of users module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    team_members: TeamMembersRepository