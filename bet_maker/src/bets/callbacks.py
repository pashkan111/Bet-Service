from fastapi import APIRouter

callback_router = APIRouter(prefix='/callback')


@callback_router.post('/event')
async def event_changed_status(data: dict):
    ...