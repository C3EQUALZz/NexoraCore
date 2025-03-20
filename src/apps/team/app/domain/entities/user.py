from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.values.user import Email, Role


@dataclass(eq=False)
class UserEntity(BaseEntity):
    email: Email
    role: Role = field(default_factory=lambda: Role("staffer"))
