from app.domain.entities.team import TeamEntity
from app.exceptions.infrastructure import TeamNotFoundException, AttributeException, TeamAlreadyExistsException
from app.infrastructure.uow.teams.base import TeamsUnitOfWork


class TeamsService:
    def __init__(self, uow: TeamsUnitOfWork) -> None:
        self._uow = uow

    async def add(self, team: TeamEntity) -> TeamEntity:
        async with self._uow as uow:
            if await self.check_existence(name=team.name.as_generic_type()):
                raise TeamAlreadyExistsException(team.name.as_generic_type())

            new_team: TeamEntity = await uow.teams.add(team)
            await uow.commit()
            return new_team

    async def get_by_name(self, name: str) -> TeamEntity:
        async with self._uow as uow:
            team: TeamEntity | None = await uow.teams.get_by_team_name(name)

            if not team:
                raise TeamNotFoundException(name)

            return team

    async def update(self, oid: str, model: TeamEntity) -> TeamEntity:
        async with self._uow as uow:
            team: TeamEntity | None = await uow.teams.get(oid)

            if not team:
                raise TeamNotFoundException(oid)

            team: TeamEntity | None = await uow.teams.update(oid, model)

            await uow.commit()

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

    async def get_all(self, start: int = 0, limit: int = 10) -> list[TeamEntity]:
        async with self._uow as uow:
            return await uow.teams.list(start=start, limit=limit)

    async def check_existence(
            self,
            oid: str | None = None,
            name: str | None = None,
    ) -> bool:
        if not (oid or name):
            raise AttributeException("Please provide oid or name existence checking")

        async with self._uow as uow:
            team: TeamEntity | None

            if name:
                team: TeamEntity | None = await uow.teams.get_by_team_name(name)
                if team:
                    return True

            if oid:
                team: TeamEntity | None = await uow.teams.get(oid)
                if team:
                    return True

            return False
