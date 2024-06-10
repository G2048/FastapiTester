import asyncio
import json
from json import JSONDecodeError
from typing import TypeAlias

from httpx import AsyncClient

Json: TypeAlias = str


class Parser:
    def __init__(self, swagger_info: dict):
        self.swagger_info = swagger_info


class Surrogate:
    def __init__(self, url):
        self._client = AsyncClient
        self.url = url
        self.file = 'openapi.json'

    @staticmethod
    def _jsonValidate(response):
        try:
            return response.json()
        except JSONDecodeError:
            return None

    async def response(self) -> Json:
        async with self._client() as client:
            response = await client.get(self.url)
            json_data = self._jsonValidate(response)
            if not json_data:
                raise RuntimeError(f"Can't get data from {self.url}")
            return json_data

    def save_to_file(self, json_info: Json) -> None:
        with open(self.file, 'w') as f:
            json.dump(json_info, f)

    def load_from_file(self) -> dict:
        try:
            with open(self.file) as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def serialize(self, swagger_info: Json) -> dict:
        return json.dumps(swagger_info)

    async def get(self):
        swagger_info: dict = self.load_from_file()
        if not swagger_info:
            swagger_info: Json = await self.response()
            self.save_to_file(swagger_info)
            swagger_info = self.serialize(swagger_info)
        return swagger_info


class Swagger:
    def __init__(self, url='http://127.0.0.1:8000/openapi.json'):
        self.url = url
        self._proxy = Surrogate(url)

    async def get(self) -> dict:
        return await self._proxy.get()

    async def parse(self, parser: Parser):
        swagger_info = await self._proxy.get()
        return Parser(swagger_info)


async def main():
    swagger = Swagger()
    swagger_info = await swagger.get()
    print(swagger_info)
    paths = swagger_info['paths']
    print(paths.keys())


if __name__ == '__main__':
    asyncio.run(main())
