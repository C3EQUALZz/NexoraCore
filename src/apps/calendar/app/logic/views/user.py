from datetime import datetime

from app.infrastructure.services.tasks import TasksService
from app.infrastructure.uow.events.base import EventsUnitOfWork


class UserView:
    def __init__(self, uow: EventsUnitOfWork) -> None:
        self._uow = uow

    async def is_user_is_available(self, user_oid: str, start_time: datetime, end_time: datetime) -> bool:
        task_service: TasksService = TasksService(self._uow)
        return await task_service.is_user_available(user_id=user_oid, start_time=start_time, end_time=end_time)
