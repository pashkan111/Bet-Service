from .provider_integration import get_event
from .schemas import BetCreateSchema, MakeBetSchema


async def get_bet_data(data: MakeBetSchema) -> BetCreateSchema:
    event = await get_event(data.event_id)
    bet = BetCreateSchema(
        event_id=data.event_id,
        event_state=event['state'],
        coefficient=event['coefficient'],
        price=data.price,
        )
    return bet
    