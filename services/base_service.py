import logging

import aiohttp

logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self, access_token):
        self.access_token = access_token

    async def make_request(self, method, url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Error making request to {url}: {response.status}")
                    return None
