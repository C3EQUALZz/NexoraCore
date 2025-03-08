from pydantic import BaseModel, BeforeValidator, PlainSerializer, Field
from uuid import UUID
from typing import Annotated

StringUUID = Annotated[
    UUID,
    BeforeValidator(lambda x: UUID(x) if isinstance(x, str) else x),
    PlainSerializer(lambda x: str(x)),
    Field(
        description="Better annotation for UUID, parses from string format. Serializes to string format."
    ),
]

class CreateTeamMemberSchema(BaseModel):
    user_id: StringUUID
    position: str
    superiors: list[StringUUID] = Field(default_factory=list)
    subordinates: list[StringUUID] = Field(default_factory=list)


