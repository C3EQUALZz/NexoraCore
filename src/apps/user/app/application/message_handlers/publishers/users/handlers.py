import logging

from app.application.message_handlers.publishers.users.schemas import UserDeleteEventSchemaResponse

logger = logging.getLogger(__name__)


async def send_delete_user_event(oid: str) -> UserDeleteEventSchemaResponse:
    ...
