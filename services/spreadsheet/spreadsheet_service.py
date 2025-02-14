from openpyxl import Workbook

from config.logger_config import LoggerConfig


class SpreadsheetService:
    def __init__(self, columns, logger: LoggerConfig):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(columns + ["Origem"])
        self.ws.auto_filter.ref = self.ws.dimensions
        self.logger = logger.get_logger(__name__)

    def append_row(self, row):
        self.ws.append(row)

    def save(self, filename):
        self.wb.save(filename)
        self.logger.info(f"Centralized spreadsheet saved as '{filename}'")
