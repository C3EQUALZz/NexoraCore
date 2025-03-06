from abc import (
    ABC,
    abstractmethod,
)

from app.domain.entities.team_members import TeamMemberEntity
from app.infrastructure.repositories.base import AbstractRepository


class TeamMembersRepository(AbstractRepository[TeamMemberEntity], ABC):
    """
    An interface for work with team members, that is used by TeamUnitOfWork.
    The main goal is that implementations of this interface can be easily replaced in TeamUnitOfWork
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> TeamMemberEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: TeamMemberEntity) -> TeamMemberEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> TeamMemberEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: TeamMemberEntity) -> TeamMemberEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> list[TeamMemberEntity]:
        raise NotImplementedError
