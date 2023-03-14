import urllib.parse
from abc import ABC

import aiohttp
from aiohttp_retry import RetryClient, RetryOptionsBase


class AsyncRESTFetcher(ABC):
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

    async def _handle_response(self, response: aiohttp.ClientResponse):
        try:
            return await response.json()
        except Exception:
            return await response.text()

    async def _fetch(
        self, url: str, data: dict | None = None
    ):
        retry_options = RetryOptionsBase(
            attempts=self.retry_attemps,
            retry_all_server_errors=True,
        )
        async with aiohttp.ClientSession() as session:
            client = RetryClient(session, retry_options=retry_options)
            async with client.request(
                method=self.method,
                url=url,
                json=data,
            ) as response:
                response.raise_for_status()
                fetched_data = await self._handle_response(response)
                return fetched_data

    async def make_request(self, data: dict | None = None):
        url = self._get_url()
        response = await self._fetch(url, data)
        return response
