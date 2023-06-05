from fastapi import APIRouter, exceptions

from .managers import BetManager, EventManager
from .schemas import BetCreateSchema
from .services import create_bet

bets_router = APIRouter(prefix='/bets')


@bets_router.get('/')
async def get_bets_route():
    bets = await BetManager.get_bets()
    return bets


@bets_router.post('/', status_code=201)
async def create_bet_route(data: BetCreateSchema):
    try:
        bet = await create_bet(data)
    except Exception as e:
        raise exceptions.HTTPException(status_code=400, detail=str(e))
    return bet


@bets_router.get('/events')
async def get_events_route():
    events = await EventManager.get_events()
    return events
