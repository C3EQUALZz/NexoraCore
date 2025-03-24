from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class TaskCreatedEvent(AbstractEvent):
    ...


@dataclass(frozen=True)
class TaskUpdatedEvent(AbstractEvent):
    ...
