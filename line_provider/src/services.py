from .schemas import EventSchema
from config import settings
import urllib.parse
import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient


async def send_callback(data: dict, callback_url: str, method: str = 'POST'):
    retry_options = {
        'attempts': 5,
        'start_timeout': 2,
        'statuses': [500, 502, 503, 504],
        'exceptions': [aiohttp.ClientConnectionError]
    }
    async with aiohttp.ClientSession() as session:
        client = RetryClient(session, retries=ExponentialRetry(**retry_options))
        async with client.request(method=method, url=callback_url, json=data) as response:
            response.raise_for_status()


def make_url(base_url: str, endpoint: str):
    return urllib.parse.urljoin(base_url, endpoint)


async def send_event_state_to_bet_maker(data: EventSchema):
    url = make_url(settings.BET_MAKER_CALLBACKS_URL, settings.BET_MAKER_CHANGE_EVENT_STATUS_ENDPOINT)
    await send_callback(data.dict(include={'event_id', 'state'}), url) 
