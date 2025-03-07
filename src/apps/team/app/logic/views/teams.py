from app.domain.entities.team import TeamEntity
from app.infrastructure.services.teams import TeamsService
from app.infrastructure.uow.teams.base import TeamsUnitOfWork


class TeamsView:
    def __init__(self, uow: TeamsUnitOfWork) -> None:
        self._uow = uow

    async def get_team_by_id(self, team_id: str) -> TeamEntity:
        teams_service: TeamsService = TeamsService(self._uow)
        team: TeamEntity = await teams_service.get(team_id)
        return team

    async def get_team_by_name(self, team_name: str) -> TeamEntity:
        teams_service: TeamsService = TeamsService(self._uow)
        team: TeamEntity = await teams_service.get_by_name(team_name)
        return team

    async def get_all_teams(self, page_number: int = 1, page_size: int = 10) -> list[TeamEntity]:
        teams_service: TeamsService = TeamsService(self._uow)
        start: int = (page_number - 1) * page_size
        limit: int = start + page_size
        teams: list[TeamEntity] = await teams_service.get_all(start, limit)
        return teams
