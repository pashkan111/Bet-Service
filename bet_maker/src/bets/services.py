from .managers import BetManager, EventManager
from .schemas import BetCreateSchema


async def create_bet(data: BetCreateSchema):
    event = await EventManager.get_event_by_id(data.event_id)
    bet = await BetManager.create_bet(data, event.coefficient)
    return bet
