from services.file_processing.strategies.file_processing_strategy import (
    FileProcessingStrategy,
)


class FileProcessor:
    """
    Class responsible for processing files using a specified strategy.

    Attributes:
        session (aiohttp.ClientSession): The HTTP client session.
        ws (openpyxl.worksheet.worksheet.Worksheet): The worksheet to append data to.
        access_token (str): The access token for authentication.
        drive_id (str): The ID of the drive containing the file.
        strategy (FileProcessingStrategy): The strategy to process the file.
    """

    def __init__(
        self, session, ws, access_token, drive_id, strategy: FileProcessingStrategy
    ):
        """
        Initializes the FileProcessor with the specified parameters.

        Args:
            session (aiohttp.ClientSession): The HTTP client session.
            ws (openpyxl.worksheet.worksheet.Worksheet): The worksheet to append data to.
            access_token (str): The access token for authentication.
            drive_id (str): The ID of the drive containing the file.
            strategy (FileProcessingStrategy): The strategy to process the file.
        """
        self.session = session
        self.ws = ws
        self.access_token = access_token
        self.drive_id = drive_id
        self.strategy = strategy

    async def process_file(self, file):
        """
        Processes the file using the specified strategy.

        Args:
            file (dict): The file metadata.
        """
        await self.strategy.process(
            file, self.session, self.ws, self.access_token, self.drive_id
        )
