import logging
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Dict, Any

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.uow.base import AbstractUnitOfWork

logger = logging.getLogger(__name__)


@dataclass
class BaseConsumer(ABC):
    def __init__(self, broker: BaseMessageBroker, uow: AbstractUnitOfWork) -> None:
        self._broker = broker
        self._uow = uow

    @property
    @abstractmethod
    def topic(self) -> str:
        """Возвращает имя топика для подписки"""
        raise NotImplementedError

    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> None:
        """Обработка полученного сообщения"""
        raise NotImplementedError

    async def start_consuming(self) -> None:
        """Основной цикл потребления сообщений"""
        async for msg in self._broker.start_consuming(self.topic):  # type: ignore
            try:
                await self.process_message(msg)
            except Exception as e:
                logger.error(f"Ошибка обработки сообщения: {e}", exc_info=True)
