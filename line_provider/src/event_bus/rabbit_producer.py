import logging
from collections.abc import AsyncGenerator

import aio_pika
from config import settings

from .schemas import BaseMessage

logger = logging.getLogger(__name__)


async def get_connection() -> AsyncGenerator[aio_pika.RobustConnection, None]:
    connection = await aio_pika.connect_robust(
        f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@rabbitmq/"
    )
    async with connection:
        yield connection


async def publish_message(
        message: BaseMessage, routing_key: str
):
    async for connection in get_connection():
        exchange_name = settings.BET_MAKER_EXCHANGE
        channel = await connection.channel()
        exchange = await channel.declare_exchange(exchange_name)

        sended_message = await exchange.publish(
            aio_pika.Message(
                body=message.json().encode('utf-8'),
                content_type="text/plain",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key,
        )
        logger.info(f"Message {sended_message} sent to {exchange_name} with routing key {routing_key}")
