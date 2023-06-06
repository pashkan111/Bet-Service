from fastapi import APIRouter
from src.utils.abstract_response import response_decorator

from .managers import BetManager, EventManager
from .schemas import BetCreateSchema

bets_router = APIRouter(prefix='/bets')


@bets_router.get('/')
@response_decorator
async def get_bets_route():
    bets = await BetManager.get_bets()
    return bets


@bets_router.post('/', status_code=201)
@response_decorator
async def create_bet_route(data: BetCreateSchema):
    bet = await BetManager.place_bet(data)
    return bet


@bets_router.get('/events')
@response_decorator
async def get_events_route():
    events = await EventManager.get_events()
    return events
