from typing import Self

from app.infrastructure.repositories.team_members.alchemy import SQLAlchemyTeamMembersRepository
from app.infrastructure.repositories.team_members.base import TeamMembersRepository
from app.infrastructure.repositories.team.alchemy import SQLAlchemyTeamsRepository
from app.infrastructure.repositories.team.base import TeamsRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.teams.base import TeamsUnitOfWork


class SQLAlchemyTeamsUnitOfWork(SQLAlchemyAbstractUnitOfWork, TeamsUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.teams: TeamsRepository = SQLAlchemyTeamsRepository(session=self._session)
        self.team_members: TeamMembersRepository = SQLAlchemyTeamMembersRepository(session=self._session)
        return uow
