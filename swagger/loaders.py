import json
from abc import ABC, abstractmethod

from api import BaseApi, Json


class SwaggerLoader(ABC):

    @abstractmethod
    def get(self):
        pass


class HttpLoader(SwaggerLoader, BaseApi):

    async def get(self):
        swagger_info: Json = await self._response()
        if not swagger_info:
            raise RuntimeError(f"Can't get data from {self.URL}")

        return self.serialize(swagger_info)


class ProxyLoader(HttpLoader):

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
