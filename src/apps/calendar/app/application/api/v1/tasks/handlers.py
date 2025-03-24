from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from uuid import UUID

from fastapi.params import Depends
from starlette import status

from app.application.api.v1.auth.dependencies import RoleChecker
from app.application.api.v1.tasks.schemas import CreateTaskSchemaRequest, UpdateTaskSchemaRequest, TaskSchemaResponse
from app.domain.entities.events.task import TaskEntity
from app.infrastructure.uow.events.base import EventsUnitOfWork
from app.logic.bootstrap import Bootstrap
from app.logic.commands.tasks import CreateTaskCommand, DeleteTaskCommand, UpdateTaskCommand
from app.logic.message_bus import MessageBus
from app.logic.views.tasks import TasksView

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    route_class=DishkaRoute
)


@router.get(
    "/{task_id}/",
    description="Get task in calendar by ID",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RoleChecker(allowed_roles=["admin", "user", "manager"]))]
)
async def get_task_in_calendar(
        task_id: UUID,
        uow: FromDishka[EventsUnitOfWork]
) -> TaskSchemaResponse:
    view: TasksView = TasksView(uow=uow)
    task: TaskEntity = await view.get_task_by_id(str(task_id))
    return TaskSchemaResponse.from_entity(task)


@router.get(
    "/",
    description="Get all tasks in calendar",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RoleChecker(allowed_roles=["admin", "user", "manager"]))]
)
async def get_all_tasks_in_calendar(
        uow: FromDishka[EventsUnitOfWork],
        page_number: int = Query(1, ge=1, description="Number of page"),
        page_size: int = Query(10, ge=1, description="Size of page")
) -> list[TaskSchemaResponse]:
    view: TasksView = TasksView(uow=uow)
    tasks: list[TaskEntity] = await view.get_all_tasks(page_number, page_size)
    return [TaskSchemaResponse.from_entity(x) for x in tasks]


@router.post(
    "/",
    description="Create new task in calendar",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RoleChecker(allowed_roles=["admin", "user", "manager"]))]
)
async def create_task_in_calendar(
        schema: CreateTaskSchemaRequest,
        bootstrap: FromDishka[Bootstrap[EventsUnitOfWork]]
) -> TaskSchemaResponse:
    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(CreateTaskCommand(**schema.model_dump()))
    return TaskSchemaResponse.from_entity(message_bus.command_result)


@router.put(
    "/{task_id}/",
    description="Update task in calendar",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RoleChecker(allowed_roles=["admin", "user", "manager"]))]
)
async def update_task_in_calendar(
        task_id: UUID,
        schema: UpdateTaskSchemaRequest,
        bootstrap: FromDishka[Bootstrap[EventsUnitOfWork]]
) -> TaskSchemaResponse:
    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(UpdateTaskCommand(**{"oid": str(task_id), **schema.model_dump()}))
    return TaskSchemaResponse.from_entity(message_bus.command_result)


@router.delete(
    "/{task_id}/",
    description="Delete task in calendar",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(allowed_roles=["admin", "user", "manager"]))]
)
async def delete_task_in_calendar(
        task_id: UUID,
        bootstrap: FromDishka[Bootstrap[EventsUnitOfWork]]
) -> None:
    message_bus: MessageBus = await bootstrap.get_messagebus()
    await message_bus.handle(DeleteTaskCommand(oid=str(task_id)))
    return message_bus.command_result
