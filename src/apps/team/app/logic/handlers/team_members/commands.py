from typing import override
from app.logic.commands.team_members import CreateTeamMemberCommand, UpdateTeamMemberCommand, DeleteTeamMemberCommand
from app.logic.handlers.team_members.base import TeamMembersCommandHandler


class CreateTeamMemberCommandHandler(TeamMembersCommandHandler[CreateTeamMemberCommand]):

    @override
    async def __call__(self, command: CreateTeamMemberCommand) -> None:
        ...


class UpdateTeamMemberCommandHandler(TeamMembersCommandHandler[UpdateTeamMemberCommand]):
    @override
    async def __call__(self, command: UpdateTeamMemberCommand) -> None:
        ...


class DeleteTeamMemberCommandHandler(TeamMembersCommandHandler[DeleteTeamMemberCommand]):
    @override
    async def __call__(self, command: DeleteTeamMemberCommand) -> None:
        ...
