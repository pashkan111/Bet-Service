import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient


async def send_callback(data: dict, callback_url: str, method: str | None='POST'):
    retry_options = {
        'attempts': 5,
        'start_timeout': 2,
        'statuses': [500, 502, 503, 504],
        'exceptions': [aiohttp.ClientConnectionError]
    }
    print(data)
    async with aiohttp.ClientSession() as session:
        client = RetryClient(session, retries=ExponentialRetry(**retry_options))
        async with client.request(method=method, url=callback_url, json=data) as response:
            response.raise_for_status()
