import logging
from typing import Literal
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from app.application.api.v1.task.schemas import CreateTaskSchemaRequest, UpdateTaskSchemaRequest, TaskSchemaResponse
from app.domain.entities.task import TaskEntity
from app.infrastructure.uow.task.base import TasksUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.tasks import DeleteTaskCommand, CreateTaskCommand, UpdateTaskCommand, UpdateTaskStatusCommand, \
    CreateNewCommentForTaskCommand
from app.logic.message_bus import MessageBus
from app.logic.views.task import TasksView

router = APIRouter(
    prefix="/task",
    tags=["task"],
    route_class=DishkaRoute
)

logger = logging.getLogger(__name__)


@router.get(
    "/{task_id}/",
    status_code=200,
    description="Get a task by ID",
)
async def get_task_by_id(
        uow: FromDishka[TasksUnitOfWork],
        task_id: UUID
) -> TaskSchemaResponse:
    tasks_view: TasksView = TasksView(uow=uow)
    task: TaskEntity = await tasks_view.get_task_by_id(str(task_id))
    return TaskSchemaResponse.from_entity(task)


@router.post(
    "/",
    status_code=201,
    description="Create a new task",
)
async def create_task(
        schema: CreateTaskSchemaRequest,
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]]
) -> TaskSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(CreateTaskCommand(**schema.model_dump()))
    return TaskSchemaResponse.from_entity(messagebus.command_result)


@router.put(
    "/{task_id}/",
    status_code=200,
    description="Update a task by ID",
)
async def update_task(
        task_id: UUID,
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]],
        schema: UpdateTaskSchemaRequest
) -> TaskSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(UpdateTaskCommand(**{"task_id": task_id, **schema.model_dump()}))
    return TaskSchemaResponse.from_entity(messagebus.command_result)


@router.delete(
    "/{task_id}/",
    description="Handler for deleting task by id",
    status_code=204,
)
async def delete_task(
        task_id: UUID,
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]]
) -> None:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(DeleteTaskCommand(oid=str(task_id)))
    return messagebus.command_result


@router.patch(
    "/{task_id}/status/",
    status_code=200,
    description="Update task status",
)
async def change_status_for_task(
        task_id: UUID,
        status: Literal["open", "in_progress", "completed"],
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]]
) -> TaskSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(UpdateTaskStatusCommand(task_id=str(task_id), status=status))
    return TaskSchemaResponse.from_entity(messagebus.command_result)


@router.post(
    "/{task_id}/comments/",
    status_code=200,
    description="Create a new comment for a task",
)
async def create_comment_for_task(
        task_id: UUID,
        comment: str,
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]]
) -> TaskSchemaResponse:
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(CreateNewCommentForTaskCommand(task_id=str(task_id), comment=comment))
    return TaskSchemaResponse.from_entity(messagebus.command_result)
