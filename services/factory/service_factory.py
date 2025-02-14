from auth.authentication import AuthenticationService
from config.logger_config import LoggerConfig
from config.settings import Settings
from services.file_processing.file_processor import FileProcessor
from services.file_processing.strategies.excel_processing_strategy import (
    ExcelProcessingStrategy,
)
from services.sharepoint.sharepoint_service import SharePointFolderService
from services.spreadsheet.spreadsheet_service import SpreadsheetService


class ServiceFactory:
    def __init__(self, settings: Settings, logger: LoggerConfig):
        self.settings = settings
        self.logger = logger
        self.auth_service = None
        self.sharepoint_service = None
        self.spreadsheet_service = None
        self.file_processor = None

    def get_auth_service(self):
        if not self.auth_service:
            self.auth_service = AuthenticationService(self.settings, self.logger)
        return self.auth_service

    def get_sharepoint_service(self):
        if not self.sharepoint_service:
            access_token = self.get_auth_service().get_access_token()
            self.sharepoint_service = SharePointFolderService(
                access_token, self.settings, self.logger
            )
        return self.sharepoint_service

    def get_spreadsheet_service(self):
        if not self.spreadsheet_service:
            self.spreadsheet_service = SpreadsheetService(
                self.settings.columns, self.logger
            )
        return self.spreadsheet_service

    async def get_file_processor(self, session):
        if not self.file_processor:
            strategy = ExcelProcessingStrategy()
            self.file_processor = FileProcessor(
                session,
                self.get_spreadsheet_service().ws,
                self.get_auth_service().get_access_token(),
                await self.get_sharepoint_service().get_drive_id(
                    await self.get_sharepoint_service().get_site_id()
                ),
                strategy,
            )
        return self.file_processor
