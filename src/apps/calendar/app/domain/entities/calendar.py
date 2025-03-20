from app.domain.entities.base import BaseEntity
from dataclasses import dataclass

from app.domain.entities.events.base import BaseEventCalendarEntity


@dataclass(eq=False)
class CalendarEntity(BaseEntity):
    owner_id: str
    events: list[BaseEventCalendarEntity]
