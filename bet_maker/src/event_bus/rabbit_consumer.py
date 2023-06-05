import logging
from collections.abc import AsyncGenerator

import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from config import settings

logger = logging.getLogger(__name__)


async def get_connection() -> AsyncGenerator[aio_pika.RobustConnection, None]:
    connection = await aio_pika.connect_robust(
        f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@rabbitmq/"
    )
    async with connection:
        yield connection


async def consume_messages(queue_name: str) -> AsyncGenerator[AbstractIncomingMessage, None]:
    logger.info('Start consuming...')
    async for connection in get_connection():
        channel = await connection.channel()
        try:
            exchange = await channel.get_exchange(settings.RABBITMQ_EXCHANGE)
        except aio_pika.exceptions.ChannelNotFoundEntity:
            exchange = await channel.declare_exchange(settings.RABBITMQ_EXCHANGE)

        queue = await channel.declare_queue(queue_name, auto_delete=True)
        await queue.bind(exchange)

        async with queue.iterator() as queue_iter:
            async for msg in queue_iter:
                async with msg.process():
                    yield msg
