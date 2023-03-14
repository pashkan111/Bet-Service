import urllib.parse

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient
from pydantic import BaseModel, ValidationError

from . import exceptions


class AsyncRESTFetcher:
    base_url: str
    endpoint: str
    response_model: type[BaseModel]
    method: str = 'GET'
    retry_attemps: int = 5

    def __init__(self, base_url, endpoint, response_model, method=None):
        self.base_url = base_url
        self.endpoint = endpoint
        self.response_model = response_model
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
                    fetched_data = await response.json()
                    return fetched_data
        except aiohttp.ClientConnectorError as e:
            raise exceptions.ConnectionError(str(e))
        
        except (aiohttp.client.ServerConnectionError) as e:
            raise exceptions.RemoteServerError(str(e))

    def _parse_response(self, data: dict | list):
        try:
            if isinstance(data, dict):
                return self.response_model(**data)
            elif isinstance(data, list):
                return self.response_model(*data)
        except ValidationError:
            pass

    async def make_request(self, data: dict | None = None):
        url = self._get_url()
        response = await self._fetch(url, data)
        return response
