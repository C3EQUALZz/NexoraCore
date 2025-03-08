from uuid import UUID
from typing import Self
from pydantic import BaseModel, Field, EmailStr


class UserSchemaResponse(BaseModel):
    oid: UUID
    surname: str = Field(min_length=1, max_length=50)
    patronymic: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr

    @classmethod
    def from_(cls, oid: str, surname: str, patronymic: str, name: str, email: str) -> Self:
        return cls(
            oid=UUID(oid),
            surname=surname,
            patronymic=patronymic,
            name=name,
            email=email  # type: ignore
        )
