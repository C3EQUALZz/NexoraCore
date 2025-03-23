from app.domain.entities.user import UserEntity
from app.infrastructure.services.user import UserService
from app.logic.events.user import UserDeletedEvent, UserCreatedEvent, UserUpdatedEvent
from app.logic.handlers.users.base import UsersEventHandler


class UserDeletedEventHandler(UsersEventHandler[UserDeletedEvent]):
    async def __call__(self, event: UserDeletedEvent) -> None:
        user_service = UserService(uow=self._uow)
        await user_service.delete(event.user_oid)


class UserCreatedEventHandler(UsersEventHandler[UserCreatedEvent]):
    async def __call__(self, event: UserCreatedEvent) -> None:
        user_service = UserService(uow=self._uow)
        user: UserEntity = UserEntity(oid=event.user_oid)
        await user_service.add(user)


class UserUpdatedEventHandler(UsersEventHandler[UserUpdatedEvent]):
    async def __call__(self, event: UserUpdatedEvent) -> None:
        user_service = UserService(uow=self._uow)
        user: UserEntity = UserEntity(oid=event.user_oid)
        await user_service.update(user)
