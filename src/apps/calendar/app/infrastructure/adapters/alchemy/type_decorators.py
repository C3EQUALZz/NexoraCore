from sqlalchemy import TypeDecorator, UUID
import uuid

class StringUUID(TypeDecorator):
    """Кастомный тип для преобразования UUID в строку при загрузке и строки в UUID при сохранении."""
    impl = UUID(as_uuid=True)
    cache_ok = True

    def process_bind_param(self, value: str, dialect) -> UUID:
        if isinstance(value, str):
            return uuid.UUID(value)

    def process_result_value(self, value: UUID, dialect) -> str:
        if value:
            return str(value)