from app.logic.events.users import UserDeleteEvent, UserCreateEvent
from app.logic.handlers.users.base import UsersEventHandler


class UserDeleteEventHandler(UsersEventHandler):
    async def __call__(self, event: UserDeleteEvent) -> None:
        await self._broker.send_message(
            topic="delete-user",
            value=await event.to_broker_message(),
            key=str(event.oid).encode(),
        )


class UserCreateEventHandler(UsersEventHandler):
    async def __call__(self, event: UserCreateEvent) -> None:
        await self._broker.send_message(
            topic="create-user",
            value=await event.to_broker_message(),
            key=str(event.oid).encode(),
        )

