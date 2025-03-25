from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.user import Role, Email


@dataclass(eq=False)
class UserEntity(BaseEntity):
    email: Email
    role: Role
