from datetime import datetime

from pydantic import BaseModel, Field
from typing import Literal, Self, cast

from app.application.api.v1.utils.schemas import StringUUID, UserSchemaResponse
from app.domain.entities.events.task import TaskEntity


class CreateTaskSchemaRequest(BaseModel):
    title: str = Field(
        ...,
        description="Название задачи. Краткий заголовок, отражающий суть задачи."
    )
    description: str | None = Field(
        None,
        description="Описание задачи. Дополнительные детали или комментарии к задаче (необязательное поле)."
    )
    assignee_id: StringUUID = Field(
        ...,
        description="Уникальный идентификатор пользователя (UUID), которому назначена задача."
    )
    start_time: datetime = Field(
        ...,
        description="Дата и время начала задачи. Определяет, когда задача должна быть начата."
    )
    end_time: datetime = Field(
        ...,
        description="Дата и время окончания задачи. Определяет, когда задача должна быть выполнена."
    )
    created_by_id: StringUUID = Field(
        ...,
        description="Уникальный идентификатор пользователя (UUID), который создал задачу. Это поле полезно для аудита и отслеживания истории создания."
    )


class UpdateTaskSchemaRequest(CreateTaskSchemaRequest):
    status: Literal["pending", "in_progress", "completed"] = Field(
        ...,
        description="Статус выполнения задачи"
    )


class TaskSchemaResponse(BaseModel):
    oid: StringUUID = Field(
        ...,
        description="ID задания"
    )

    title: str = Field(
        ...,
        description="Название задачи. Краткий заголовок, отражающий суть задачи."
    )
    description: str | None = Field(
        None,
        description="Описание задачи. Дополнительные детали или комментарии к задаче (необязательное поле)."
    )
    assignee: UserSchemaResponse = Field(
        ...,
        description="Пользователь, которому назначена задача."
    )
    start_time: datetime = Field(
        ...,
        description="Дата и время начала задачи. Определяет, когда задача должна быть начата."
    )
    end_time: datetime = Field(
        ...,
        description="Дата и время окончания задачи. Определяет, когда задача должна быть выполнена."
    )
    created_by: UserSchemaResponse = Field(
        ...,
        description="Пользователь, который создал задачу. Это поле полезно для аудита и отслеживания истории создания."
    )

    status: Literal["pending", "in_progress", "completed"] = Field(
        ...,
        description="Статус выполнения задачи"
    )

    @classmethod
    def from_entity(cls, entity: TaskEntity) -> Self:
        return cls(
            oid=entity.oid,
            title=entity.title,
            description=entity.description,
            assignee=UserSchemaResponse.from_entity(entity.assignee),
            start_time=entity.start_time,
            end_time=entity.end_time,
            created_by=UserSchemaResponse.from_entity(entity.created_by),
            status=cast(Literal["pending", "in_progress", "completed"], entity.status),
        )
