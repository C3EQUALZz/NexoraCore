import logging

from faststream.rabbit import RabbitRouter

from app.application.message_handlers.publishers.users.schemas import UserSchemaResponse

router = RabbitRouter(prefix="users")
logger = logging.getLogger(__name__)


@router.publisher("delete-queue")
async def send_delete_user_event(
        oid: str,
        name: str,
        surname: str,
        patronymic: str,
        email: str,
) -> UserSchemaResponse:

    logger.info(f"Sending delete user event with {oid}")

    return UserSchemaResponse.from_(
        oid=oid,
        surname=surname,
        name=name,
        patronymic=patronymic,
        email=email
    )
