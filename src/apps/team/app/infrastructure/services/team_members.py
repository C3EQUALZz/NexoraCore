from typing import overload

from app.domain.entities.team import TeamEntity
from app.domain.entities.team_members import TeamMemberEntity
from app.exceptions.infrastructure import UserAlreadyExistsInTeamException, UserDoesntExistsInThisTeamException
from app.infrastructure.uow.teams.base import TeamsUnitOfWork


class TeamMembersService:
    def __init__(self, uow: TeamsUnitOfWork) -> None:
        self._uow = uow

    async def get_by_user_id(self, team_id: str, user_id: str) -> TeamMemberEntity:
        async with self._uow as uow:
            if not await self.check_existence(team_oid=team_id, team_member_oid=user_id):
                raise UserDoesntExistsInThisTeamException(team_id=team_id, user_id=user_id)

            return await uow.team_members.get_by_user_id(team_id=team_id, user_id=user_id)

    async def add(self, team_member: TeamMemberEntity, team_oid: str) -> TeamMemberEntity:
        async with self._uow as uow:
            if await self.check_existence(team_member.oid, team_oid):
                raise UserAlreadyExistsInTeamException(team_id=team_oid, user_id=team_member.oid)

            await uow.team_members.add(team_member)
            await uow.commit()

            return team_member

    @overload
    async def check_existence(self, team_member_oid: str, team_oid: str) -> bool:
        ...

    @overload
    async def check_existence(self, team_member_oid: str, team_name: str) -> bool:
        ...

    async def check_existence(
            self,
            team_member_oid: str,
            team_oid: str | None = None,
            team_name: str | None = None,
    ) -> bool:
        if team_oid is None and team_name is None:
            raise AttributeError("team oid or team name must be specified")

        async with self._uow as uow:
            if team_oid:
                if await uow.team_members.is_exists_in_team(user_id=team_member_oid, team_id=team_oid):
                    return True

            if team_name:
                team: TeamEntity = await uow.teams.get_by_team_name(team_name)
                if team and await uow.team_members.is_exists_in_team(user_id=team_member_oid, team_id=team.oid):
                    return True

            return False

    async def delete_user_in_team(self, team_id: str, user_id: str) -> None:
        async with self._uow as uow:
            if not await self.check_existence(team_oid=team_id, team_member_oid=user_id):
                raise UserDoesntExistsInThisTeamException(user_id=user_id, team_id=team_id)

            return await uow.team_members.delete_by_user_id_and_team_id(team_id=team_id, user_id=user_id)

    async def get_all_in_team(self, team_id: str, start: int = 0, limit: int = 10) -> list[TeamMemberEntity]:
        async with self._uow as uow:
            return await uow.team_members.get_all_members_in_team(team_id=team_id, start=start, limit=limit)

    async def get_all(self, start: int = 0, limit: int = 10) -> list[TeamMemberEntity]:
        async with self._uow as uow:
            return await uow.team_members.list(start=start, limit=limit)
