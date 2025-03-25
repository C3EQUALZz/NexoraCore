import builtins
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
    async def get_by_user_id(self, team_id: str, user_id: str) -> TeamMemberEntity | None:
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
    async def is_exists_in_team(self, user_id: str, team_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> list[TeamMemberEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_user_id_and_team_id(self, user_id: str, team_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_members_in_team(
            self,
            team_id: str,
            start: int | None = None,
            limit: int | None = None
    ) -> builtins.list[TeamMemberEntity]:
        raise NotImplementedError
