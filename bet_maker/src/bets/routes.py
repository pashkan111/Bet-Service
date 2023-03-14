from fastapi import APIRouter

from .managers import BetManager
from .schemas import MakeBetSchema
from .services import get_bet_data

router = APIRouter(prefix='/bets')


@router.get('/')
async def get_bets():
    bets = await BetManager.get_bets()
    return bets


@router.post('/', status_code=201)
async def create_bet(data: MakeBetSchema):
    bet_data = await get_bet_data(data)
    created_bet = await BetManager.create_bet(bet_data)
    return created_bet
