from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class UserDeletedEvent(AbstractEvent):
    user_oid: str


@dataclass(frozen=True)
class UserCreatedEvent(AbstractEvent):
    user_oid: str


@dataclass(frozen=True)
class UserUpdatedEvent(AbstractEvent):
    user_oid: str
