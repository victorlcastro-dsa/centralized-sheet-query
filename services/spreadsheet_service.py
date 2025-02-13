import logging

from openpyxl import Workbook

logger = logging.getLogger(__name__)


class SpreadsheetService:
    def __init__(self, columns):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(columns + ["Origem"])
        self.ws.auto_filter.ref = self.ws.dimensions

    def append_row(self, row):
        self.ws.append(row)

    def save(self, filename):
        self.wb.save(filename)
        logger.info(f"Centralized spreadsheet saved as '{filename}'")
