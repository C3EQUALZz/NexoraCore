from app.logic.events.base import AbstractEvent
from dataclasses import dataclass


@dataclass(frozen=True)
class PublishNewTideEvent(AbstractEvent):
    email: str

