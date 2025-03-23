from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Set, Dict, Any

from app.domain.entities.events.base import BaseEventCalendarEntity
from app.domain.entities.user import UserEntity


@dataclass(eq=False)
class MeetingEntity(BaseEventCalendarEntity):
    organizer: UserEntity
    participants: list[UserEntity] = field(default_factory=list)
    start_time: datetime = field(default_factory=lambda: datetime.now())
    end_time: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=1))

    async def to_dict(
            self,
            exclude: Optional[Set[str]] = None,
            include: Optional[Dict[str, Any]] = None,
            save_classes_value_objects: bool = False,
    ) -> Dict[str, Any]:

        data: Dict[str, Any] = await super().to_dict(
            exclude=exclude,
            include=include,
            save_classes_value_objects=save_classes_value_objects
        )

        data["organizer_id"] = data.pop("organizer").get("oid")

        return data
