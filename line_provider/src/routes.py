from fastapi.routing import APIRouter

from . import schemas
from .exceptions import EventNotFoundException

events = {
    1: schemas.EventSchema(coefficient=1.77, deadline=169675645342, event_id=1),
    2: schemas.EventSchema(coefficient=1.56, deadline=169675645333, event_id=2),
    3: schemas.EventSchema(coefficient=3.66, deadline=169675645366, event_id=3),
}

event_router = APIRouter(prefix='/events')


@event_router.post("/")
async def create_event(event: schemas.CreateEventSchema):
    event_id = len(events) + 1
    db_event = schemas.EventSchema(**event.dict(), event_id=event_id)
    events[event_id] = db_event
    return db_event


@event_router.get("/")
async def get_events():
    return [event for event in events.values()]


@event_router.put("/{event_id}")
async def update_event(event_id: int, event: schemas.CreateEventSchema):
    db_event = events.get(event_id)
    if not db_event:
        raise EventNotFoundException
    db_event = db_event.copy(update=dict(event))
    events[event_id] = db_event
    return db_event


@event_router.get("/{event_id}")
async def get_event(event_id: int):
    event_id.append(1)
    db_event = events.get(event_id)
    if not db_event:
        raise EventNotFoundException
    return db_event
