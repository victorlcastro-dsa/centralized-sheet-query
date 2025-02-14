from abc import ABC, abstractmethod
from io import BytesIO

from config.logger_config import LoggerConfig

logger = LoggerConfig.get_logger(__name__)


class BaseFileProcessingStrategy(ABC):
    """
    Abstract base class for file processing strategies.

    Attributes:
        file_extension (str): The file extension that this strategy can process.
    """

    def __init__(self, file_extension):
        """
        Initializes the BaseFileProcessingStrategy with the specified file extension.

        Args:
            file_extension (str): The file extension that this strategy can process.
        """
        self.file_extension = file_extension

    async def process(self, file, session, ws, access_token, drive_id):
        """
        Processes the file if it matches the specified file extension.

        Args:
            file (dict): The file metadata.
            session (aiohttp.ClientSession): The HTTP client session.
            ws (openpyxl.worksheet.worksheet.Worksheet): The worksheet to append data to.
            access_token (str): The access token for authentication.
            drive_id (str): The ID of the drive containing the file.
        """
        if file["name"].endswith(self.file_extension):
            file_id = file["id"]
            logger.info(f"Processing file: {file['name']}")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}/content"
            async with session.get(url, headers=headers) as file_response:
                if file_response.status == 200:
                    file_content = BytesIO(await file_response.read())
                    await self.process_content(file_content, file, ws)
                else:
                    logger.error(
                        f"Error downloading file {file['name']}: {file_response.status}"
                    )
                    logger.error(f"Response: {await file_response.text()}")

    @abstractmethod
    async def process_content(self, file_content, file, ws):
        """
        Abstract method to process the content of the file.

        Args:
            file_content (BytesIO): The content of the file.
            file (dict): The file metadata.
            ws (openpyxl.worksheet.worksheet.Worksheet): The worksheet to append data to.
        """
        pass
