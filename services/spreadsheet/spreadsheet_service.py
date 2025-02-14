from typing import Any, List

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from config.logger_config import LoggerConfig


class SpreadsheetService:
    """
    Service class for manipulating spreadsheets.

    Attributes:
        wb (Workbook): The workbook instance.
        ws (Worksheet): The active worksheet instance.
        logger (Logger): Logger instance.
    """

    def __init__(
        self, columns: List[str], origin_column_name: str, logger: LoggerConfig
    ) -> None:
        """
        Initializes the SpreadsheetService with columns, origin column name, and logger.

        Args:
            columns (List[str]): List of column names for the spreadsheet.
            origin_column_name (str): Name of the origin column.
            logger (LoggerConfig): Logger configuration.
        """
        self.wb: Workbook = Workbook()
        self.ws: Worksheet = self.wb.active
        self.ws.append(columns + [origin_column_name])
        self.ws.auto_filter.ref = self.ws.dimensions
        self.logger = logger.get_logger(__name__)

    def append_row(self, row: List[Any]) -> None:
        """
        Appends a row to the active worksheet.

        Args:
            row (List[Any]): The row data to append.
        """
        self.ws.append(row)

    def save(self, filename: str) -> None:
        """
        Saves the workbook to the specified filename.

        Args:
            filename (str): The name of the file to save the workbook as.
        """
        self.wb.save(filename)
        self.logger.info(f"Centralized spreadsheet saved as '{filename}'")
