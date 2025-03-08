from typing import Self, Annotated
import uuid

from pydantic import BaseModel, Field, AfterValidator, UUID4

from app.domain.entities.team import TeamEntity


class CreateTeamSchemaRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)

class UpdateTeamSchemaRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)


class TeamResponse(BaseModel):
    oid: UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))]
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)

    @classmethod
    def from_entity(cls, entity: TeamEntity) -> Self:
        return cls(
            oid=entity.oid,
            name=entity.name.as_generic_type(),
            description=entity.description.as_generic_type()
        )
