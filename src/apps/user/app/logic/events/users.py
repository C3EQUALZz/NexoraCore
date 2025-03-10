from app.logic.events.base import AbstractEvent
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class UserCreateEvent(AbstractEvent):
    oid: str
    email: str
    surname: str
    name: str
    patronymic: str


@dataclass(frozen=True)
class UserDeleteEvent(AbstractEvent):
    user_oid: str
