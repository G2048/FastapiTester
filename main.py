import asyncio
import json
from json import JSONDecodeError
from typing import TypeAlias

from httpx import AsyncClient

Json: TypeAlias = str


class Parser:

    def __init__(self, swagger_info: dict):
        self.swagger_info = swagger_info


class SwaggerLoader:

    def __init__(self, url):
        self._client = AsyncClient
        self.url = url

    @staticmethod
    def _jsonValidate(response):
        try:
            return response.json()
        except JSONDecodeError:
            return None

    @staticmethod
    def serialize(swagger_info: Json) -> dict:
        return json.loads(swagger_info)

    async def _response(self) -> Json:
        async with self._client() as client:
            response = await client.get(self.url)
            json_data = self._jsonValidate(response)
            if not json_data:
                raise RuntimeError(f"Can't get data from {self.url}")
            return json_data

    async def get(self):
        swagger_info: Json = await self._response()
        return self.serialize(swagger_info)


class ProxyLoader(SwaggerLoader):

    def __init__(self, url):
        super().__init__(url)
        self.file = 'openapi.json'

    def save_to_file(self, json_info: Json) -> None:
        with open(self.file, 'w') as f:
            json.dump(json_info, f)

    def load_from_file(self) -> dict | None:
        try:
            with open(self.file) as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    async def get(self):
        swagger_info: dict = self.load_from_file()
        if not swagger_info:
            swagger_info: Json = await self._response()
            self.save_to_file(swagger_info)
            swagger_info = self.serialize(swagger_info)
        return swagger_info


class Swagger:

    def __init__(self, loader: SwaggerLoader):
        self._loader = loader

    async def get(self) -> dict:
        return await self._loader.get()

    async def parse(self, parser: Parser):
        swagger_info = await self._loader.get()
        return Parser(swagger_info)


async def main():
    url = 'http://127.0.0.1:8000/openapi.json'
    proxy_json = ProxyLoader(url)
    swagger = Swagger(proxy_json)
    swagger_info = await swagger.get()
    print(swagger_info)
    paths = swagger_info['paths']
    print(paths.keys())


if __name__ == '__main__':
    asyncio.run(main())
