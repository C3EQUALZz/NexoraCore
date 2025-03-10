from app.domain.entities.base import BaseEntity
from dataclasses import dataclass
from datetime import datetime

from app.domain.values.task import Title, Description, TaskStatus
from app.domain.values.shared import Comment


@dataclass(eq=False)
class Task(BaseEntity):
    """
    Domain which represents a task for user in company.
    """
    title: Title
    description: Description
    assigned_to: str
    created_by: str
    due_date: datetime
    status: TaskStatus
    comments: list[Comment]
