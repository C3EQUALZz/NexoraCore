from typing import Literal, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, FutureDatetime, BeforeValidator, PlainSerializer

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
