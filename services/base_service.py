from abc import ABC, abstractmethod

import aiohttp

from config.logger_config import LoggerConfig

logger = LoggerConfig.get_logger(__name__)


class BaseService(ABC):
    def __init__(self, access_token):
        self.access_token = access_token

    async def make_request(self, method, url):
        headers = self.get_headers()
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers) as response:
                return await self.handle_response(response)

    @abstractmethod
    def get_headers(self):
        pass

    @abstractmethod
    async def handle_response(self, response):
        pass
