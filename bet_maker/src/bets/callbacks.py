from fastapi import APIRouter, Depends

from db import AsyncSession, get_session

from .managers import BetManager
from .schemas import CallbackUpdateStateSchema

callback_router = APIRouter(prefix='/callback')


@callback_router.post('/event')
async def event_changed_status(
    data: CallbackUpdateStateSchema, session: AsyncSession = Depends(get_session)
    ):
    """Calling when event changes in line_provider service"""
    await BetManager.update_bets_event_state(data, session)
    return 200
