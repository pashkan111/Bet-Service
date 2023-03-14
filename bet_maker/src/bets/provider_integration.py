
from config import settings
from src.utils import AsyncRESTFetcher


async def get_events():
    fetcher = AsyncRESTFetcher(
        settings.PROVEDER_BASE_URL, '/events'
    )
    events = await fetcher.make_request()
    return events


async def get_event(event_id: int):
    fetcher = AsyncRESTFetcher(
        settings.PROVEDER_BASE_URL, f'/events/{event_id}'
    )
    event = await fetcher.make_request()
    return event
