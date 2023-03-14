import urllib.parse

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient

from . import exceptions


class AsyncRESTFetcher:
    base_url: str
    endpoint: str
    method: str = 'GET'
    retry_attemps: int = 5

    def __init__(self, base_url, endpoint, method=None):
        self.base_url = base_url
        self.endpoint = endpoint
        if method:
            self.method = method

    def _get_url(self) -> str:
        return urllib.parse.urljoin(self.base_url, self.endpoint)

    async def _fetch(
        self, url: str, data: dict | None = None
    ):
        retry_options = {
            'attempts': self.retry_attemps,
            'start_timeout': 1,
            'statuses': [500, 502, 503, 504],
            'exceptions': [aiohttp.ClientConnectionError]
        }
        try:
            async with aiohttp.ClientSession() as session:
                client = RetryClient(session, retries=ExponentialRetry(**retry_options))
                async with client.request(method=self.method, url=url, json=data) as response:
                    data = await self._handle_response(response)
                    return data

        except aiohttp.ClientConnectorError as e:
            raise exceptions.ConnectionError(str(e))

        except (aiohttp.client.ServerConnectionError) as e:
            raise exceptions.RemoteServerError(str(e))
        
    async def _handle_response(self, response: aiohttp.ClientResponse):
        data = await response.json()
        if response.status >= 400:
            raise exceptions.ClientError(data['detail'])
        return data

    async def make_request(self, data: dict | None = None) -> dict | list:
        url = self._get_url()
        fetched_data = await self._fetch(url, data)
        return fetched_data
