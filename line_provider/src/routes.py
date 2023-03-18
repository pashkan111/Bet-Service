from fastapi import BackgroundTasks
from fastapi.routing import APIRouter
from src.event_bus.rabbit_producer import publish_message
from src.event_bus.schemas import EventChangedMessage

from . import schemas
from .exceptions import EventNotFoundException
from .services import send_event_state_to_bet_maker

events = {
    1: schemas.EventSchema(coefficient=1.77, deadline=1696756453, event_id=1),
    2: schemas.EventSchema(coefficient=1.56, deadline=1696756483, event_id=2),
    3: schemas.EventSchema(coefficient=3.66, deadline=1696756753, event_id=3),
    4: schemas.EventSchema(coefficient=3.66, deadline=1023333833, event_id=4),
    5: schemas.EventSchema(coefficient=3.66, deadline=1699999953, event_id=5),
}

event_router = APIRouter(prefix='/events')


@event_router.post("/", status_code=201)
async def create_event(event: schemas.CreateEventSchema):
    event_id = len(events) + 1
    db_event = schemas.EventSchema(**event.dict(), event_id=event_id)
    events[event_id] = db_event
    return db_event


@event_router.get("/")
async def get_events():
    return [event for event in events.values()]


@event_router.patch("/{event_id}")
async def update_event(
    event_id: int, 
    event: schemas.UpdateEventSchema,
    # background_task: BackgroundTasks,
    ):
    db_event = events.get(event_id)
    if not db_event:
        raise EventNotFoundException
    db_event = db_event.copy(update=event.dict(exclude_unset=True))
    events[event_id] = db_event
    await publish_message(EventChangedMessage(data=db_event), 'bet_service')
    # background_task.add_task(send_event_state_to_bet_maker, db_event)
    return db_event


@event_router.get("/{event_id}")
async def get_event(event_id: int):
    db_event = events.get(event_id)
    if not db_event:
        raise EventNotFoundException
    return db_event
