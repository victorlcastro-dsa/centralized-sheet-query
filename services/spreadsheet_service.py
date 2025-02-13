import logging

from openpyxl import Workbook

logger = logging.getLogger(__name__)


class SpreadsheetService:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["Coluna1", "Coluna2", "Coluna3", "Origem"])
        self.ws.auto_filter.ref = self.ws.dimensions

    def append_row(self, row):
        self.ws.append(row)

    def save(self, filename):
        self.wb.save(filename)
        logger.info(f"Centralized spreadsheet saved as '{filename}'")
