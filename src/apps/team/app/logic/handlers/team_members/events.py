import logging
from typing import override

from app.logic.events.team_members import PublishNewTideEvent
from app.logic.handlers.teams.base import TeamsEventHandler

logger = logging.getLogger(__name__)


class PublishNewTideEventHandler(TeamsEventHandler[PublishNewTideEvent]):
    @override
    async def __call__(self, event: PublishNewTideEvent) -> None:

        logger.info("Sending email notification into broker to user: %s", event.email)

        await self._broker.send_message(
            topic="email-notifications",
            value=await event.to_broker_message(),
            key=str(event.oid).encode()
        )
