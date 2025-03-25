from app.infrastructure.repositories.base import AbstractRepository
from app.domain.entities.team import TeamEntity
from abc import ABC, abstractmethod


class TeamsRepository(AbstractRepository[TeamEntity], ABC):
    """
    An interface for work with team members, that is used by TeamUnitOfWork.
    The main goal is that implementations of this interface can be easily replaced in TeamUnitOfWork
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_team_name(self, name: str) -> TeamEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: TeamEntity) -> TeamEntity:
        raise NotImplementedError

    @abstractmethod
    async def get(self, oid: str) -> TeamEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, oid: str, model: TeamEntity) -> TeamEntity:
        raise NotImplementedError

    @abstractmethod
    async def list(self, start: int = 0, limit: int = 10) -> list[TeamEntity]:
        raise NotImplementedError
