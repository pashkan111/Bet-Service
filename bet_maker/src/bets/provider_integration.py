
from config import settings
from src.utils import AsyncRESTFetcher


async def get_events():
    fetcher = AsyncRESTFetcher(
        settings.PROVEDER_BASE_URL, '/events'
    )
    events = await fetcher.make_request()
    return events
