from fastapi import APIRouter
from .schemas import CallbackUpdateStateSchema
from .managers import BetManager


callback_router = APIRouter(prefix='/callback')


@callback_router.post('/event')
async def event_changed_status(data: CallbackUpdateStateSchema):
    """Calling when event changes in line_provider service"""
    await BetManager.update_bets_event_state(data)
    return 200
