from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute
from uuid import UUID

from app.application.api.task.schemas import CreateTaskSchemaRequest

router = APIRouter(
    prefix="/task",
    tags=["task"],
    route_class=DishkaRoute
)


@router.get("/{task_id}")
async def get_task_by_id(task_id: UUID):
    ...


@router.post("/")
async def create_task(schema: CreateTaskSchemaRequest):
    ...


@router.put("/{task_id}")
async def update_task(task_id: UUID):
    ...


@router.delete("/{task_id}")
async def delete_task(task_id: UUID):
    ...


@router.patch("/{task_id}/status")
async def change_status_for_task(task_id: UUID):
    ...


@router.post("/{task_id}/comments")
async def create_comment_for_task(task_id: UUID):
    ...


