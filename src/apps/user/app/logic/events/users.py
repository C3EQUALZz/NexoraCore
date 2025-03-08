from app.logic.events.base import AbstractEvent
from dataclasses import dataclass


@dataclass(frozen=True)
class UserCreatedEvent(AbstractEvent):
    oid: str
    email: str
    surname: str
    name: str
    patronymic: str


@dataclass(frozen=True)
class UserDeleteEvent(AbstractEvent):
    oid: str
