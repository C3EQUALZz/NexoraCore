import logging
from uuid import UUID
from typing import Literal

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException

from app.application.api.v1.task.schemas import CreateTaskSchemaRequest, UpdateTaskSchemaRequest, TaskSchemaResponse
from app.domain.entities.task import TaskEntity
from app.exceptions.base import ApplicationException
from app.infrastructure.uow.task.base import TasksUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.tasks import DeleteTaskCommand, CreateTaskCommand, UpdateTaskCommand, UpdateTaskStatusCommand
from app.logic.message_bus import MessageBus
from app.logic.views.task import TasksView

router = APIRouter(
    prefix="/task",
    tags=["task"],
    route_class=DishkaRoute
)

logger = logging.getLogger(__name__)


@router.get(
    "/{task_id}",
    status_code=200,
)
async def get_task_by_id(
        uow: FromDishka[TasksUnitOfWork],
        task_id: UUID
) -> TaskSchemaResponse:
    try:
        tasks_view: TasksView = TasksView(uow=uow)
        task: TaskEntity = await tasks_view.get_task_by_id(str(task_id))
        return TaskSchemaResponse.from_entity(task)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.post("/")
async def create_task(
        schema: CreateTaskSchemaRequest,
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]]
):
    try:
        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(CreateTaskCommand(**schema.model_dump()))
        return TaskSchemaResponse.from_entity(messagebus.command_result)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.put("/{task_id}")
async def update_task(
        task_id: UUID,
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]],
        schema: UpdateTaskSchemaRequest
) -> TaskSchemaResponse:
    try:
        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(UpdateTaskCommand(**{"task_id": task_id, **schema.model_dump()}))
        return TaskSchemaResponse.from_entity(messagebus.command_result)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.delete("/{task_id}")
async def delete_task(
        task_id: UUID,
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]]
) -> None:
    try:
        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(DeleteTaskCommand(oid=str(task_id)))
        return messagebus.command_result
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.patch("/{task_id}/status")
async def change_status_for_task(
        task_id: UUID,
        status: Literal["open", "in_progress", "completed"],
        bootstrap: FromDishka[Bootstrap[TasksUnitOfWork]]
) -> TaskSchemaResponse:
    try:
        messagebus: MessageBus = await bootstrap.get_messagebus()
        await messagebus.handle(UpdateTaskStatusCommand(task_id=str(task_id), status=status))
        return TaskSchemaResponse.from_entity(messagebus.command_result)
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))


@router.post("/{task_id}/comments")
async def create_comment_for_task(
        task_id: UUID,
        comment: str
):
    try:
        ...
    except ApplicationException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status, detail=str(e))
