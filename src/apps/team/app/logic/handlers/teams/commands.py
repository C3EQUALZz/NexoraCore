from typing import override

from app.domain.entities.team import TeamEntity
from app.domain.values.team import TeamName, TeamDescription
from app.infrastructure.services.teams import TeamsService
from app.logic.commands.team import CreateTeamCommand, UpdateTeamCommand, DeleteTeamCommand
from app.logic.handlers.teams.base import TeamsCommandHandler


class CreateTeamCommandHandler(TeamsCommandHandler[CreateTeamCommand]):
    @override
    async def __call__(self, command: CreateTeamCommand) -> TeamEntity:
        teams_service = TeamsService(self._uow)

        new_team: TeamEntity = TeamEntity(
            name=TeamName(command.name),
            description=TeamDescription(command.description),
        )

        return await teams_service.add(new_team)


class UpdateTeamCommandHandler(TeamsCommandHandler[UpdateTeamCommand]):
    @override
    async def __call__(self, command: UpdateTeamCommand) -> TeamEntity:
        teams_service = TeamsService(self._uow)

        old_team: TeamEntity = await teams_service.get(oid=command.oid)

        updated_team: TeamEntity = TeamEntity(
            name=TeamName(command.name),
            description=TeamDescription(command.description),
            members=old_team.members,
        )

        updated_team.oid = old_team.oid

        return await teams_service.update(command.oid, updated_team)


class DeleteTeamCommandHandler(TeamsCommandHandler[DeleteTeamCommand]):
    @override
    async def __call__(self, command: DeleteTeamCommand) -> None:
        teams_service = TeamsService(self._uow)
        return await teams_service.delete(oid=command.oid)
