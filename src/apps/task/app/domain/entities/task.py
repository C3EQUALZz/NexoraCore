from app.domain.entities.base import BaseEntity
from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping, Any, Self
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

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> Self:
        title: Title = Title(document["title"])
        description: Description = Description(document["description"])
        assigned_to: str = document["assigned_to"]
        created_by: str = document["created_by"]
        due_datetime: datetime = document["due_datetime"]
        status: TaskStatus = TaskStatus(document["status"])
        comments: list[Comment] = [Comment(x) for x in document["comments"]]

        return cls(
            title=title,
            description=description,
            assigned_to=assigned_to,
            created_by=created_by,
            due_datetime=due_datetime,
            status=status,
            comments=comments,
        )
