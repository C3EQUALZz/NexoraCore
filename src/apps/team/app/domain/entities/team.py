from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.entities.team_members import TeamMemberEntity
from app.domain.values.team import TeamName, TeamDescription
from typing import Self, Mapping, Any


@dataclass(eq=False)
class TeamEntity(BaseEntity):
    name: TeamName
    description: TeamDescription
    members: list[TeamMemberEntity] = field(default_factory=list)

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> Self:
        oid: str = document["oid"]
        name: TeamName = TeamName(document["name"])
        description: TeamDescription = TeamDescription(document["description"])

        if document.get("members", None):
            members: list[TeamMemberEntity] = [TeamMemberEntity.from_document(x) for x in document["members"]]
        else:
            members: list[TeamMemberEntity] = []

        return cls(oid=oid, name=name, description=description, members=members)
