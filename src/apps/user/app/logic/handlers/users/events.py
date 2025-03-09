import asyncio

from app.application.message_handlers.publishers.users.handlers import send_delete_user_event
from app.logic.events.users import UserDeleteEvent
from app.logic.handlers.users.base import UsersEventHandler


class UserDeleteEventHandler(UsersEventHandler):
    async def __call__(self, event: UserDeleteEvent) -> None:
        asyncio.create_task(send_delete_user_event(**await event.to_dict()))
