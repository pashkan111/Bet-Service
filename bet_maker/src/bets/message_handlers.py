import abc
import logging

from config import settings
from pydantic import BaseModel, ValidationError
from src.bets.managers import EventManager
from src.bets.schemas import EventSchema
from src.event_bus.rabbit_consumer import consume_messages
from src.event_bus.schemas import BaseMessage

logger = logging.getLogger(__name__)


class AbstractMessageHandler(abc.ABC):
    schema: type[BaseModel]

    @abc.abstractclassmethod
    async def handle_message(cls, message: dict):
        ...


class EventChangedHandler(AbstractMessageHandler):
    """Handler for event changed message"""
    schema = EventSchema

    @classmethod
    async def handle_message(cls, message: dict):
        data = cls.schema(**message)
        await EventManager.update_event_data(data)
        logger.info(f'EVENT CHANGED. Data: {data.dict()}')


class EventCreateHandler(AbstractMessageHandler):
    """Handler for event created message"""
    schema = EventSchema

    @classmethod
    async def handle_message(cls, message: dict):
        data = cls.schema(**message)
        await EventManager.create_event(data)
        logger.info(f'EVENT CREATED. Data: {data.dict()}')


class MessageHandler:
    handlers: dict[int, type[AbstractMessageHandler]] = {
        1001: EventChangedHandler,
        1002: EventCreateHandler
    }

    def _get_handler(self, message_id: int) -> type[AbstractMessageHandler]:
        try:
            return self.handlers[message_id]
        except KeyError:
            logger.error(f'No handler for message_id: {message_id}')
            raise

    def _validate_message(self, message: bytes) -> BaseMessage:
        try:
            return BaseMessage.parse_raw(message)
        except ValidationError as e:
            logger.error(f'Invalid message: {e}')
            raise

    async def get_messages(self):
        async for msg in consume_messages(settings.RABBITMQ_EVENTS_QUEUE):
            loaded_msg = self._validate_message(msg.body)
            handler = self._get_handler(loaded_msg.message_id)
            print(loaded_msg.data)
            await handler.handle_message(loaded_msg.data)


message_handler = MessageHandler()
