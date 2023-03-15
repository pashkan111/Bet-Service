from config import settings
from src.utils import AsyncRESTFetcher

from .constants import EventSchema, EventsSchema


async def get_events() -> EventsSchema:
    fetcher = AsyncRESTFetcher(settings.PROVIDER_BASE_URL, '/events')
    events = await fetcher.make_request()
    return EventsSchema(__root__=events)


async def get_event(event_id: int) -> EventSchema:
    fetcher = AsyncRESTFetcher(settings.PROVIDER_BASE_URL, f'/events/{event_id}')
    event = await fetcher.make_request()
    return EventSchema(**event)
