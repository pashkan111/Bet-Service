import time

from src.utils.error_handler import error_handler

from .constants import EventSchema
from .provider_integration import get_event, get_events
from .schemas import BetCreateSchema, MakeBetSchema


@error_handler
async def get_bet_data(data: MakeBetSchema) -> BetCreateSchema:
    event = await get_event(data.event_id)
    bet = BetCreateSchema(
        event_id=data.event_id,
        event_state=event.state,
        coefficient=event.coefficient,
        price=data.price,
        )
    return bet


@error_handler
async def get_available_events() -> list[EventSchema]:
    events = await get_events()
    current_timestamp = time.time()
    filtered_events = list(filter(lambda event: event.deadline > current_timestamp, events.__root__))
    return filtered_events
