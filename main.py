import asyncio

from configs import get_logger
from swagger import ProxyLoader, SwaggerLoader

logger = get_logger()


class Parser:

    def __init__(self, swagger_info: dict):
        self.swagger_info = swagger_info


class Swagger:

    def __init__(self, loader: SwaggerLoader):
        self._loader = loader

    @property
    def version(self):
        return 'openapi'

    @property
    def info(self):
        return 'info'

    @property
    def paths(self):
        return 'paths'

    async def get(self) -> dict:
        return await self._loader.get()

    async def parse(self, parser: Parser):
        swagger_info = await self._loader.get()
        return Parser(swagger_info)


class Tester:
    """The Constructed a request for testing the swagger API"""

    def __init__(self, swagger: SwaggerLoader):
        self.swagger_info = swagger.get()

    # Class
    def __request(self):
        pass


async def main():
    url = 'http://127.0.0.1:8000/openapi.json'
    proxy_loader = ProxyLoader(url)
    swagger = Swagger(proxy_loader)
    swagger_info = await swagger.get()
    logger.info(swagger_info)
    paths = swagger_info['paths']
    logger.debug(paths.keys())
    logger.debug(swagger.info)


if __name__ == '__main__':
    asyncio.run(main())
