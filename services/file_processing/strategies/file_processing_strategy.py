from abc import ABC, abstractmethod
from typing import Any, Dict

import aiohttp
from openpyxl.worksheet.worksheet import Worksheet


class FileProcessingStrategy(ABC):
    """
    Abstract base class for file processing strategies.

    Methods:
        process(file, session, ws, access_token, drive_id): Processes the file.
    """

    @abstractmethod
    async def process(
        self,
        file: Dict[str, Any],
        session: aiohttp.ClientSession,
        ws: Worksheet,
        access_token: str,
        drive_id: str,
    ) -> None:
        """
        Abstract method to process the file.

        Args:
            file (dict): The file metadata.
            session (aiohttp.ClientSession): The HTTP client session.
            ws (Worksheet): The worksheet to append data to.
            access_token (str): The access token for authentication.
            drive_id (str): The ID of the drive containing the file.
        """
        pass
