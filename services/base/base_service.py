from abc import ABC, abstractmethod

import aiohttp

from config.logger_config import LoggerConfig

logger = LoggerConfig.get_logger(__name__)


class BaseService(ABC):
    """
    Abstract base class for services that make HTTP requests.

    Attributes:
        access_token (str): Access token for authentication.
    """

    def __init__(self, access_token):
        """
        Initializes the BaseService class with an access token.

        Args:
            access_token (str): Access token for authentication.
        """
        self.access_token = access_token

    async def make_request(self, method, url):
        """
        Makes an HTTP request with the specified method and URL.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            url (str): URL for the request.

        Returns:
            dict: JSON response from the request.
        """
        headers = self.get_headers()
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers) as response:
                return await self.handle_response(response)

    @abstractmethod
    def get_headers(self):
        """
        Returns the headers for the HTTP request.

        Returns:
            dict: Headers for the request.
        """
        pass

    @abstractmethod
    async def handle_response(self, response):
        """
        Handles the response from the HTTP request.

        Args:
            response (aiohttp.ClientResponse): Response from the request.

        Returns:
            dict: Processed response data.
        """
        pass
