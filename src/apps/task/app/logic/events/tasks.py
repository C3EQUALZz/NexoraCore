from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class TaskCreatedEvent(AbstractEvent):
    task_id: str
    email_assigned_to: str
