import asyncio
import json

from pydantic import BaseModel
from src.bets.managers import BetManager
from src.bets.schemas import CallbackUpdateStateSchema
from src.event_bus.rabbit_consumer import consume_messages


class AbstractMessageHandler:
    schema: type[BaseModel]

    @classmethod
    async def handle_message(cls, message: dict):
        ...


class EventChangedHandler(AbstractMessageHandler):
    schema = CallbackUpdateStateSchema

    @classmethod
    async def handle_message(cls, message: dict):
        print(message)
        data = cls.schema(**message['data'])
        await BetManager.update_bets_event_state(data)
        print(data)
        print('EVENT UPDAATED')


class MessageHandler:
    handlers: dict[int, type[AbstractMessageHandler]] = {
        1001: EventChangedHandler
    }

    def _get_handler(self, message_id: int) -> type[AbstractMessageHandler]:
        return self.handlers[message_id]

    async def get_messages(self):
        async for msg in consume_messages('bet_service'):
            loaded_msg = json.loads(msg.body)
            handler = self._get_handler(loaded_msg['message_id'])
            await handler.handle_message(loaded_msg)
            await asyncio.sleep(0.1)


message_handler = MessageHandler()
