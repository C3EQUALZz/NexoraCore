from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.user import Email, Password, Role, Status


@dataclass(eq=False)
class UserEntity(BaseEntity):
    surname: str
    name: str
    patronymic: str
    email: Email
    password: Password
    role: Role
    status: Status


