from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.user import Role


@dataclass(eq=False)
class UserEntity(BaseEntity):
    role: Role
