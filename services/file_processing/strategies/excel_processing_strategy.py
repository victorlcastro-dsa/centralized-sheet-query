import pandas as pd

from config.logger_config import LoggerConfig
from services.file_processing.strategies.base_file_processing_strategy import (
    BaseFileProcessingStrategy,
)

logger = LoggerConfig.get_logger(__name__)


class ExcelProcessingStrategy(BaseFileProcessingStrategy):
    """
    Strategy for processing Excel files.

    Methods:
        process_content(file_content, file, ws): Processes the content of an Excel file.
    """

    def __init__(self):
        """
        Initializes the ExcelProcessingStrategy with the .xlsx file extension.
        """
        super().__init__(".xlsx")

    async def process_content(self, file_content, file, ws):
        """
        Processes the content of an Excel file.

        Args:
            file_content (BytesIO): The content of the file.
            file (dict): The file metadata.
            ws (openpyxl.worksheet.worksheet.Worksheet): The worksheet to append data to.
        """
        df = pd.read_excel(file_content)
        if not df.empty:
            for row in df.itertuples(index=False, name=None):
                ws.append(row + (file["name"],))
            logger.info(f"File {file['name']} processed successfully")
        else:
            logger.warning(f"File {file['name']} is empty")
