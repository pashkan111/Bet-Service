from collections.abc import AsyncGenerator

import aio_pika
from aio_pika import ExchangeType

from .schemas import BaseMessage


async def get_connection() -> AsyncGenerator[aio_pika.RobustConnection, None]:
    connection = await aio_pika.connect_robust(
        f"amqp://bet_service:password@rabbitmq/"
    )
    async with connection:
        yield connection


async def publish_message(
        message: BaseMessage, routing_key: str
    ):
    async for connection in get_connection():
        channel = await connection.channel()
        
        # exchange = await channel.declare_exchange(ExchangeType.DIRECT)
        # queue = await channel.declare_queue(auto_delete=True)

        # await queue.bind(exchange, routing_key)

        sended = await channel.default_exchange.publish(
            aio_pika.Message(
                body=message.json().encode('utf-8'),
                content_type="text/plain",
            ),
            routing_key,
        )
        print(sended)
