from dataclasses import dataclass, field

from app.domain.entities.events.base import BaseEventCalendarEntity
from app.domain.entities.user import UserEntity


@dataclass(eq=False)
class MeetingEntity(BaseEventCalendarEntity):
    organizer_id: str
    participants: list[UserEntity] = field(default_factory=list)

    def is_participant(self, user_id: str) -> bool:
        return user_id in self.participants or user_id == self.organizer_id

    def is_organizer(self, user_id: str) -> bool:
        return user_id == self.organizer_id
