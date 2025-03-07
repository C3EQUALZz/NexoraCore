from typing import Self

from app.infrastructure.repositories.team_members.alchemy import SQLAlchemyTeamMembersRepository
from app.infrastructure.repositories.team_members.base import TeamMembersRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.team_members.base import TeamMembersUnitOfWork


class SQLAlchemyTeamMembersUnitOfWork(SQLAlchemyAbstractUnitOfWork, TeamMembersUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.team_members: TeamMembersRepository = SQLAlchemyTeamMembersRepository(session=self._session)
        return uow
