from openpyxl import Workbook

from config.logger_config import LoggerConfig


class SpreadsheetService:
    """
    Service class for manipulating spreadsheets.

    Attributes:
        wb (Workbook): The workbook instance.
        ws (Worksheet): The active worksheet instance.
        logger (Logger): Logger instance.
    """

    def __init__(self, columns, origin_column_name, logger: LoggerConfig):
        """
        Initializes the SpreadsheetService with columns, origin column name, and logger.

        Args:
            columns (list): List of column names for the spreadsheet.
            origin_column_name (str): Name of the origin column.
            logger (LoggerConfig): Logger configuration.
        """
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(columns + [origin_column_name])
        self.ws.auto_filter.ref = self.ws.dimensions
        self.logger = logger.get_logger(__name__)

    def append_row(self, row):
        """
        Appends a row to the active worksheet.

        Args:
            row (list): The row data to append.
        """
        self.ws.append(row)

    def save(self, filename):
        """
        Saves the workbook to the specified filename.

        Args:
            filename (str): The name of the file to save the workbook as.
        """
        self.wb.save(filename)
        self.logger.info(f"Centralized spreadsheet saved as '{filename}'")
