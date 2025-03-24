from datetime import datetime
from typing import Literal, Annotated, Self, cast
from uuid import UUID

from pydantic import BaseModel, Field, FutureDatetime, BeforeValidator, PlainSerializer

from app.domain.entities.task import TaskEntity

StringUUID = Annotated[
    UUID,
    BeforeValidator(lambda x: UUID(x) if isinstance(x, str) else x),
    PlainSerializer(lambda x: str(x)),
    Field(
        description="Better annotation for UUID, parses from string format. Serializes to string format."
    ),
]


class CreateTaskSchemaRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
        description="Name of task, give a brief description"
    )

    description: str = Field(
        min_length=1,
        max_length=500,
        description="Description of task, here manager provides detailed description"
    )

    assigned_to: UUID = Field(description="User id to whom the task should be assigned")
    created_by: UUID = Field(description="User id to whom the task should be created")
    due_datetime: FutureDatetime = Field(description="Due date of task")


class UpdateTaskSchemaRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
        description="Name of task, give a brief description"
    )

    description: str = Field(
        min_length=1,
        max_length=500,
        description="Description of task, here manager provides detailed description"
    )

    assigned_to: UUID = Field(description="User id to whom the task should be assigned")
    created_by: UUID = Field(description="User id to whom the task should be created")
    due_datetime: FutureDatetime = Field(description="Due date of task")
    status: Literal["open", "in_progress", "completed"] = Field(description="Status of task")


class TaskSchemaResponse(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="Name of task, give a brief description")
    description: str = Field(min_length=1, max_length=500,
                             description="Description of task, here manager provides detailed description")
    assigned_to: UUID = Field(description="User id to whom the task should be assigned")
    created_by: UUID = Field(description="User id to whom the task should be created")
    due_datetime: datetime = Field(description="Due date of task")
    status: Literal["open", "in_progress", "completed"] = Field(description="Status of task")

    @classmethod
    def from_entity(cls, entity: TaskEntity) -> Self:
        return cls(
            title=entity.title.as_generic_type(),
            description=entity.description.as_generic_type(),
            assigned_to=UUID(entity.assigned_to),
            created_by=UUID(entity.created_by),
            due_datetime=entity.due_datetime,
            status=cast(Literal["open", "in_progress", "completed"], entity.status.as_generic_type()),
        )
