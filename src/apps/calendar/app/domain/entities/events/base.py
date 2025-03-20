from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class BaseEventCalendarEntity(ABC, BaseEntity):
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    created_by: str  # Кто создал
    owner_id: str  # Чей календарь (пользователя или команды)

    def duration(self):
        return self.end_time - self.start_time
