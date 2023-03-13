import uuid

from fastapi.routing import APIRouter

from . import schemas
from .exceptions import EventNotFoundException

events = {}

event_router = APIRouter(prefix='/events')


@event_router.post("/")
async def create_event(event: schemas.CreateEventSchema):
    db_event = schemas.EventSchema(**event.dict())
    events[db_event.event_id] = db_event
    return db_event


@event_router.get("/")
async def get_events():
    return [event for event in events.values()]


@event_router.put("/{event_id}")
async def update_event(event_id: uuid.UUID, event: schemas.CreateEventSchema):
    db_event = events.get(event_id)
    if not db_event:
        raise EventNotFoundException
    db_event = db_event.copy(update=dict(event))
    events[event_id] = db_event
    return db_event


@event_router.get("/{event_id}")
async def get_event(event_id: uuid.UUID):
    db_event = events.get(event_id)
    if not db_event:
        raise EventNotFoundException
    return db_event
