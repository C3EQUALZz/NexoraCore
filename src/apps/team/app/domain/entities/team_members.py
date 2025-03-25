from dataclasses import dataclass, field
from typing import Mapping, Any, Self

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class TeamMemberEntity(BaseEntity):
    user_id: str
    team_id: str
    superiors_ids: list[str] = field(default_factory=list)
    subordinates_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> Self:
        oid: str = document["oid"]
        user_id: str = document["user_id"]
        team_id: str = document["team_id"]

        if document.get("superiors_ids", None):
            superiors_ids: list[str] = document["superiors_ids"]
        else:
            superiors_ids: list[str] = []

        if document.get("subordinates_ids", None):
            subordinates_ids: list[str] = document["subordinates_ids"]
        else:
            subordinates_ids: list[str] = []

        return cls(
            oid=oid,
            team_id=team_id,
            user_id=user_id,
            superiors_ids=superiors_ids,
            subordinates_ids=subordinates_ids,
        )
