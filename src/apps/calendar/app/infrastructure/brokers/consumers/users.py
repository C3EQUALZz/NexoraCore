import logging
from typing import Dict, Any, override

from app.infrastructure.brokers.consumers.base import BaseConsumer
from app.logic.events.user import UserDeletedEvent, UserCreatedEvent, UserUpdatedEvent

logger = logging.getLogger(__name__)


class UserDeletedConsumer(BaseConsumer):
    @property
    @override
    def topic(self) -> str:
        return "delete-user"

    @override
    async def process_message(self, message: Dict[str, Any]) -> None:
        async with self._uow as uow:
            if not (user_oid := message.get("user_oid")):
                logger.error("Bad message from Kafka: there is no user_oid")
                return

            await uow.add_event(UserDeletedEvent(user_oid=user_oid))
            logger.info("delete event user, used_oid: %s was created", user_oid)


class UserCreatedConsumer(BaseConsumer):
    @property
    @override
    def topic(self) -> str:
        return "create-user"

    @override
    async def process_message(self, message: Dict[str, Any]) -> None:
        async with self._uow as uow:
            if not (user_oid := message.get("user_oid")):
                logger.error("Bad message from Kafka: there is no user_oid")
                return

            if not (role := message.get("role")):
                logger.error("Bad message from Kafka: there is no role for user")
                return

            await uow.add_event(UserCreatedEvent(user_oid=user_oid, role=role))
            logger.info("create for user %s was created", user_oid)


class UserUpdatedConsumer(BaseConsumer):
    @property
    @override
    def topic(self) -> str:
        return "update-user"

    @override
    async def process_message(self, message: Dict[str, Any]) -> None:
        async with self._uow as uow:
            if not (user_oid := message.get("user_oid")):
                logger.error("Bad message from Kafka: there is no user_oid")
                return

            if not (role := message.get("role")):
                logger.error("Bad message from Kafka: there is no role for user")
                return

            await uow.add_event(UserUpdatedEvent(user_oid=user_oid, role=role))
            logger.info("UpdatedUserEvent for user %s was created", user_oid)
