from app.domain.entities.team_members import TeamMemberEntity
from app.infrastructure.services.team_members import TeamMembersService
from app.infrastructure.uow.teams.base import TeamsUnitOfWork


class TeamMembersView:
    def __init__(self, uow: TeamsUnitOfWork) -> None:
        self._uow = uow

    async def get_by_user_id(self, team_id: str, user_id: str) -> TeamMemberEntity:
        team_members_service: TeamMembersService = TeamMembersService(self._uow)
        return await team_members_service.get_by_user_id(team_id=team_id, user_id=user_id)

    async def get_all_team_members_in_team(
            self,
            team_id: str,
            page_number: int = 1,
            page_size: int = 10
    ) -> list[TeamMemberEntity]:
        team_members_service: TeamMembersService = TeamMembersService(self._uow)
        start: int = (page_number - 1) * page_size
        limit: int = start + page_size
        team_members: list[TeamMemberEntity] = await team_members_service.get_all_in_team(team_id, start, limit)
        return team_members

    async def get_all_team_members(self, page_number: int = 1, page_size: int = 10) -> list[TeamMemberEntity]:
        team_members_service: TeamMembersService = TeamMembersService(self._uow)
        start: int = (page_number - 1) * page_size
        limit: int = start + page_size
        team_members: list[TeamMemberEntity] = await team_members_service.get_all(start, limit)
        return team_members
