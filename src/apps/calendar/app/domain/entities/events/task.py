from dataclasses import dataclass, field
from datetime import datetime, timedelta

from app.domain.entities.events.base import BaseEventCalendarEntity
from app.domain.entities.user import UserEntity


@dataclass(eq=False)
class TaskEntity(BaseEventCalendarEntity):
    assignee: UserEntity
    created_by: UserEntity
    status: str = field(default_factory=lambda: "pending")  # pending / in_progress / completed
    start_time: datetime = field(default_factory=lambda: datetime.now())
    end_time: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=7))
