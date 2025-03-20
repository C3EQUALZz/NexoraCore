from pydantic import BaseModel, BeforeValidator, PlainSerializer, Field
from uuid import UUID
from typing import Annotated, Self

from app.domain.entities.team_members import TeamMemberEntity

StringUUID = Annotated[
    UUID,
    BeforeValidator(lambda x: UUID(x) if isinstance(x, str) else x),
    PlainSerializer(lambda x: str(x)),
    Field(
        description="Better annotation for UUID, parses from string format. Serializes to string format."
    ),
]


class CreateTeamMemberSchemaRequest(BaseModel):
    user_id: StringUUID
    superiors: list[StringUUID] = Field(default_factory=list)
    subordinates: list[StringUUID] = Field(default_factory=list)


class TeamMemberSchemaResponse(BaseModel):
    user_id: StringUUID
    superiors: list[StringUUID]
    subordinates: list[StringUUID]

    @classmethod
    def from_entity(cls, member: TeamMemberEntity) -> Self:
        return cls(
            user_id=UUID(member.user_id),
            superiors=[UUID(x) for x in member.superiors_ids],
            subordinates=[UUID(x) for x in member.subordinates_ids],
        )


class CreateNewTidingRequestSchema(BaseModel):
    name: str
    description: str
    text: str
