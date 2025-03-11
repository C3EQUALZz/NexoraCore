from app.domain.entities.base import BaseEntity
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.values.task import Title, Description, TaskStatus
from app.domain.values.shared import Comment


@dataclass(eq=False)
class TaskEntity(BaseEntity):
    """
    Domain which represents a task for user in company.
    """
    title: Title
    description: Description
    assigned_to: str
    created_by: str
    due_datetime: datetime
    status: TaskStatus = field(default_factory=lambda: TaskStatus("open"))
    comments: list[Comment] = field(default_factory=list)
