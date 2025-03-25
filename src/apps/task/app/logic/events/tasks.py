from dataclasses import dataclass
from datetime import datetime

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class TaskCreatedEvent(AbstractEvent):
    task_id: str
    email_assigned_to: str
    start_datetime: datetime
    end_datetime: datetime


@dataclass(frozen=True)
class TaskUpdatedEvent(AbstractEvent):
    task_id: str
    email_assigned_to: str
    status: str
    start_datetime: datetime
    end_datetime: datetime


@dataclass(frozen=True)
class TaskDeletedEvent(AbstractEvent):
    task_id: str
