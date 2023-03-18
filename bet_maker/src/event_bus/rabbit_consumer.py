from collections.abc import AsyncGenerator

import aio_pika
from aio_pika.abc import AbstractIncomingMessage


async def get_connection() -> AsyncGenerator[aio_pika.RobustConnection, None]:
    connection = await aio_pika.connect_robust(
        f"amqp://bet_service:password@rabbitmq/"
    )
    async with connection:
        yield connection


async def consume_messages(queue_name: str) -> AsyncGenerator[AbstractIncomingMessage, None]:
    print('Start consuming...')
    async for connection in get_connection():
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        async with queue.iterator() as queue_iter:
            async for msg in queue_iter:
                async with msg.process():
                    yield msg
