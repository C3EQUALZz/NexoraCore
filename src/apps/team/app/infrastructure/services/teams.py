from app.domain.entities.team import TeamEntity
from app.exceptions.infrastructure import TeamNotFoundException
from app.infrastructure.uow.teams.base import TeamsUnitOfWork


class TeamsService:
    def __init__(self, uow: TeamsUnitOfWork) -> None:
        self._uow = uow

    async def add(self, team: TeamEntity) -> TeamEntity:
        async with self._uow as uow:
            new_team: TeamEntity = await uow.teams.add(team)
            await uow.commit()
            return new_team

    async def get_by_name(self, name: str) -> TeamEntity:
        async with self._uow as uow:
            team: TeamEntity | None = await uow.teams.get_by_team_name(name)

            if not team:
                raise TeamNotFoundException(name)

            return team

    async def get(self, oid: str) -> TeamEntity | None:
        async with self._uow as uow:
            team: TeamEntity | None = await uow.teams.get(oid)

            if not team:
                raise TeamNotFoundException(oid)

            return team

    async def delete(self, oid: str) -> None:
        async with self._uow as uow:
            team: TeamEntity | None = await uow.teams.get(oid)

            if not team:
                raise TeamNotFoundException(oid)

            await uow.teams.delete(oid)

            await uow.commit()


