from typing import Annotated, Self
from uuid import UUID

from pydantic import BeforeValidator, PlainSerializer, Field, BaseModel

from app.domain.entities.user import UserEntity

StringUUID = Annotated[
    UUID,
    BeforeValidator(lambda x: UUID(x) if isinstance(x, str) else x),
    PlainSerializer(lambda x: str(x)),
    Field(
        description="Better annotation for UUID, parses from string format. Serializes to string format."
    ),
]


class UserSchemaResponse(BaseModel):
    oid: UUID

    @classmethod
    def from_entity(cls, entity: UserEntity) -> Self:
        return cls(oid=UUID(entity.oid))
