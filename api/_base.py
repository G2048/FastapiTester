import json
from json import JSONDecodeError
from typing import TypeAlias

from httpx import AsyncClient

from configs import get_logger

logger = get_logger()

Json: TypeAlias = str


class BaseApi:

    def __init__(self, url):
        self.HEADERS = {'Content-Type': 'application/json'}
        self.URL = url
        self._status_code = None

    @staticmethod
    def _validateJson(jsondata):
        try:
            return jsondata()
        except JSONDecodeError:
            return None

    async def _request(self, url, method='GET', query_params=None, **kwargs):
        self.URL += url
        logger.debug(f'{url}, {query_params=}, {self.HEADERS=}')

        async with AsyncClient(follow_redirects=True) as client:
            self._response = await client.request(
                method=method, url=self.URL, params=query_params, headers=self.HEADERS, **kwargs
            )

            self.status_code = self._response.status_code
            logger.debug(self._response.status_code)
            logger.debug(self._response.text)

            if self._response.status_code < 300:
                response_json = self._validateJson(self._response.json)
                if response_json:
                    return response_json

    @property
    def status_code(self) -> int | None:
        return self._status_code

    @status_code.setter
    def status_code(self, value) -> None:
        self._status_code = value

    @staticmethod
    def serialize(data: Json) -> dict:
        return json.loads(data)


async def test():
    site = 'news.ycombinator.com'
    url = f'https://{site}/'
    api = BaseApi(url)
    answer = await api._request('')
    print(answer)


if __name__ == '__main__':
    import asyncio

    asyncio.run(test())
