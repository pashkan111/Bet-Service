from fastapi import APIRouter, Depends

from db import AsyncSession, get_session

from .managers import BetManager
from .schemas import MakeBetSchema
from .services import get_available_events, get_bet_data

bets_router = APIRouter(prefix='/bets')


@bets_router.get('/')
async def get_bets(session: AsyncSession = Depends(get_session)):
    bets = await BetManager.get_bets(session)
    return bets


@bets_router.post('/', status_code=201)
async def create_bet(data: MakeBetSchema, session: AsyncSession = Depends(get_session)):
    bet_data = await get_bet_data(data)
    created_bet = await BetManager.create_bet(bet_data, session)
    return created_bet


@bets_router.get('/events')
async def get_events(session: AsyncSession = Depends(get_session)):
    events = await get_available_events()
    return events
