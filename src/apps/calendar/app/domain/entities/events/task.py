from dataclasses import dataclass, field

from app.domain.entities.events.base import BaseEventCalendarEntity


@dataclass(eq=False)
class TaskEvent(BaseEventCalendarEntity):
    assignee_id: str  # кто выполняет задачу
    status: str = field(default_factory=lambda: "pending")  # pending / in_progress / completed
