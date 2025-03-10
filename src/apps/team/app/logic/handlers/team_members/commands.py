from typing import override
from itertools import chain
from app.domain.entities.team_members import TeamMemberEntity
from app.domain.values.team_members import TeamMemberPosition
from app.exceptions.infrastructure import UserDoesntExistsInThisTeamException
from app.infrastructure.services.team_members import TeamMembersService
from app.logic.commands.team_members import CreateTeamMemberCommand, UpdateTeamMemberCommand, DeleteTeamMemberCommand
from app.logic.handlers.team_members.base import TeamMembersCommandHandler


class CreateTeamMemberCommandHandler(TeamMembersCommandHandler[CreateTeamMemberCommand]):
    @override
    async def __call__(self, command: CreateTeamMemberCommand) -> TeamMemberEntity:
        team_member_service: TeamMembersService = TeamMembersService(self._uow)

        for person in chain.from_iterable([command.superiors, command.subordinates]):
            if not await team_member_service.check_existence(person, team_oid=command.team_id):
                raise UserDoesntExistsInThisTeamException(user_id=person, team_id=command.team_id)

        team_member: TeamMemberEntity = TeamMemberEntity(
            user_id=command.user_id,
            team_id=command.team_id,
            position=TeamMemberPosition(command.position),
            superiors_ids=command.superiors,
            subordinates_ids=command.subordinates,
        )

        return await team_member_service.add(team_member=team_member, team_oid=command.team_id)


class UpdateTeamMemberCommandHandler(TeamMembersCommandHandler[UpdateTeamMemberCommand]):
    @override
    async def __call__(self, command: UpdateTeamMemberCommand) -> None:
        ...


class DeleteTeamMemberCommandHandler(TeamMembersCommandHandler[DeleteTeamMemberCommand]):
    @override
    async def __call__(self, command: DeleteTeamMemberCommand) -> None:
        ...
