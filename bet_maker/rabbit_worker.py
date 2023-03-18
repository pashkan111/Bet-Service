import asyncio

from src.bets.message_handlers import message_handler

asyncio.run(message_handler.get_messages())
