from dataclasses import dataclass

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class UserEntity(BaseEntity):
    user_oid: str