from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping, Any, Self

from app.domain.entities.base import BaseEntity
from app.domain.entities.user import UserEntity
from app.domain.values.shared import Comment
from app.domain.values.task import Title, Description, TaskStatus
from app.domain.values.user import Role, Email


@dataclass(eq=False)
class TaskEntity(BaseEntity):
    """
    Domain which represents a task for user in company.
    """
    title: Title
    description: Description
    assigned_to: UserEntity
    created_by: UserEntity
    due_datetime: datetime
    status: TaskStatus = field(default_factory=lambda: TaskStatus("open"))
    comments: list[Comment] = field(default_factory=list)

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> Self:
        assigned_to: UserEntity = UserEntity(
            oid=document["assigned_to"].get("oid"),
            role=Role(document["assigned_to"].get("role")),
            email=Email(document["assigned_to"].get("email")),
        )

        created_by: UserEntity = UserEntity(
            oid=document["created_by"].get("oid"),
            role=Role(document["created_by"].get("role")),
            email=Email(document["created_by"].get("email")),
        )

        if document.get("comments", None):
            comments: list[Comment] = [Comment(x) for x in document["comments"]]
        else:
            comments: list[Comment] = []

        return cls(
            title=Title(document["title"]),
            description=Description(document["description"]),
            assigned_to=assigned_to,
            created_by=created_by,
            due_datetime=document["due_datetime"],
            status=TaskStatus(document["status"]),
            comments=comments,
        )
