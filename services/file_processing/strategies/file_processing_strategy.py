from abc import ABC, abstractmethod


class FileProcessingStrategy(ABC):
    """
    Abstract base class for file processing strategies.

    Methods:
        process(file, session, ws, access_token, drive_id): Processes the file.
    """

    @abstractmethod
    async def process(self, file, session, ws, access_token, drive_id):
        """
        Abstract method to process the file.

        Args:
            file (dict): The file metadata.
            session (aiohttp.ClientSession): The HTTP client session.
            ws (openpyxl.worksheet.worksheet.Worksheet): The worksheet to append data to.
            access_token (str): The access token for authentication.
            drive_id (str): The ID of the drive containing the file.
        """
        pass
