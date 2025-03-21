import asyncio
import logging
from itertools import chain
from typing import override

from app.domain.entities.team_members import TeamMemberEntity
from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import UserDoesntExistsInThisTeamException
from app.exceptions.logic import UserDoesntExistException
from app.infrastructure.services.team_members import TeamMembersService
from app.logic.commands.team_members import CreateTeamMemberCommand, UpdateTeamMemberCommand, DeleteTeamMemberCommand
from app.logic.commands.team_members import PublishNewTidingCommand
from app.logic.events.team_members import PublishNewTideEvent
from app.logic.handlers.team_members.base import TeamMembersCommandHandler

logger = logging.getLogger(__name__)

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


class PublishNewTidingCommandHandler(TeamMembersCommandHandler[PublishNewTidingCommand]):
    @override
    async def __call__(self, command: PublishNewTidingCommand) -> None:
        service: TeamMembersService = TeamMembersService(uow=self._uow)

        team: list[TeamMemberEntity] = await service.get_all_in_team(team_id=command.team_oid)

        tasks = (
            self.__process_user(user_oid)
            for user_oid in map(lambda member: member.user_id, team)
        )

        await asyncio.gather(*tasks)

    async def __process_user(self, user_oid: str) -> None:
        user: UserEntity | None = await self._service.get_user(user_oid=user_oid)

        if user is None:
            raise UserDoesntExistException(value=user_oid)

        await self._uow.add_event(PublishNewTideEvent(email=user.email.as_generic_type()))
