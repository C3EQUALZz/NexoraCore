from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.values.team_members import TeamMemberPosition


@dataclass(eq=False)
class TeamMemberEntity(BaseEntity):
    user_id: str
    position: TeamMemberPosition
    superiors: list["TeamMemberEntity"] = field(default_factory=list)
    subordinates: list["TeamMemberEntity"] = field(default_factory=list)
