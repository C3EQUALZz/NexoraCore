from datetime import datetime, UTC

from app.domain.entities.base import BaseEntity
from dataclasses import dataclass, field

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

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
