from .schemas import EventSchema
from .callbacks import send_callback
from config import settings
import urllib.parse


def make_url(base_url: str, endpoint: str):
    return urllib.parse.urljoin(base_url, endpoint)


async def send_event_state_to_bet_maker(data: EventSchema):
    url = make_url(settings.BET_MAKER_CALLBACKS_URL, settings.BET_MAKER_CHANGE_EVENT_STATUS_ENDPOINT)
    await send_callback(data.dict(include={'event_id', 'state'}), url) 
