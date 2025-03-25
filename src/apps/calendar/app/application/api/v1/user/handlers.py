from datetime import datetime
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.infrastructure.uow.events.base import EventsUnitOfWork
from app.logic.views.user import UserView

router = APIRouter(
    prefix="/user",
    tags=["user"],
    route_class=DishkaRoute
)


@router.get("/{user_id}/availability")
async def is_user_available(
        user_id: UUID,
        start_time: datetime,
        end_time: datetime,
        uow: FromDishka[EventsUnitOfWork],
) -> bool:
    view: UserView = UserView(uow=uow)
    return await view.is_user_is_available(str(user_id), start_time=start_time, end_time=end_time)

