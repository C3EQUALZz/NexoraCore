from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.entities.team_members import TeamMemberEntity
from app.domain.values.team import TeamName, TeamDescription


@dataclass(eq=False)
class TeamEntity(BaseEntity):
    name: TeamName
    description: TeamDescription
    members: list[TeamMemberEntity] = field(default_factory=list)
