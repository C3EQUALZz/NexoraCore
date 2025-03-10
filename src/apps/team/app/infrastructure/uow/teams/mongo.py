import logging
from typing import Self

from app.infrastructure.repositories.team.base import TeamsRepository
from app.infrastructure.repositories.team.mongo import MotorTeamsRepository
from app.infrastructure.repositories.team_members.base import TeamMembersRepository
from app.infrastructure.repositories.team_members.mongo import MotorTeamMembersRepository
from app.infrastructure.uow.base import MotorAbstractUnitOfWork
from app.infrastructure.uow.teams.base import TeamsUnitOfWork

logger = logging.getLogger(__name__)


class MotorTeamsUnitOfWork(MotorAbstractUnitOfWork, TeamsUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()

        if self._database is None:
            logger.error("Database does not exist")
            raise RuntimeError("Database does not exist")

        self.teams: TeamsRepository = MotorTeamsRepository(
            collection=self._database.get_collection("teams"),
            session=self._session
        )

        self.team_members: TeamMembersRepository = MotorTeamMembersRepository(
            collection=self._database.get_collection("team_members"),
            session=self._session
        )

        return uow
