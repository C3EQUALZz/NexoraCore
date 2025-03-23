from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Set, Dict, Any, override

from app.domain.entities.events.base import BaseEventCalendarEntity
from app.domain.entities.user import UserEntity


@dataclass(eq=False)
class TaskEntity(BaseEventCalendarEntity):
    assignee: UserEntity
    created_by: UserEntity
    status: str = field(default_factory=lambda: "pending")  # pending / in_progress / completed
    start_time: datetime = field(default_factory=lambda: datetime.now())
    end_time: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=7))

    @override
    async def to_dict(
            self,
            exclude: Optional[Set[str]] = None,
            include: Optional[Dict[str, Any]] = None,
            save_classes_value_objects: bool = False,
    ) -> Dict[str, Any]:
        converted_dictionary: Dict[str, Any] = await super().to_dict(
            exclude=exclude,
            include=include,
            save_classes_value_objects=save_classes_value_objects
        )

        converted_dictionary['assignee_id'] = converted_dictionary.pop('assignee').get('oid')
        converted_dictionary['created_by_id'] = converted_dictionary.pop('created_by').get('oid')

        return converted_dictionary
