import asyncio
import logging
from typing import List

from app.infrastructure.brokers.consumers.base import BaseConsumer

logger = logging.getLogger(__name__)

class ConsumerManager:
    def __init__(self, consumers: List[BaseConsumer]) -> None:
        self.consumers: List[BaseConsumer] = consumers
        self.tasks: List[asyncio.Task] = []

    async def start_all(self) -> None:
        for consumer in self.consumers:
            task = asyncio.create_task(consumer.start_consuming())
            self.tasks.append(task)

        logger.info(f"Started %s consumers", len(self.consumers))

    async def stop_all(self) -> None:
        for task in self.tasks:
            task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)
        logger.info(f"All tasks stopped")
