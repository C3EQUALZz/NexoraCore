from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.entities.events.meeting import MeetingEntity
from app.domain.entities.events.task import TaskEntity


@dataclass(eq=False)
class CalendarEntity(BaseEntity):
    owner_id: str
    tasks: list[TaskEntity]
    meetings: list[MeetingEntity]
