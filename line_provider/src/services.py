from src.event_bus.rabbit_producer import publish_message
from src.event_bus.schemas import BaseMessage


async def notify(message: BaseMessage, routing_key: str):
    await publish_message(message, routing_key)
