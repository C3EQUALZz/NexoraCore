from dataclasses import dataclass, field
from datetime import datetime, timedelta

from app.domain.entities.events.base import BaseEventCalendarEntity


@dataclass(eq=False)
class MeetingEntity(BaseEventCalendarEntity):
    organizer_id: str
    participants: list[str] = field(default_factory=list)
    start_time: datetime = field(default_factory=lambda: datetime.now())
    end_time: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=1))
