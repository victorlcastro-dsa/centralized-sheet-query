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
    """
    Service factory class to create and manage service instances.

    Attributes:
        settings (Settings): Application settings.
        logger (LoggerConfig): Logger configuration.
        auth_service (AuthenticationService): Authentication service instance.
        sharepoint_service (SharePointFolderService): SharePoint service instance.
        spreadsheet_service (SpreadsheetService): Spreadsheet service instance.
        file_processor (FileProcessor): File processor instance.
    """

    def __init__(self, settings: Settings, logger: LoggerConfig):
        """
        Initializes the ServiceFactory class with settings and logger.

        Args:
            settings (Settings): Application settings.
            logger (LoggerConfig): Logger configuration.
        """
        self.settings = settings
        self.logger = logger
        self.auth_service = None
        self.sharepoint_service = None
        self.spreadsheet_service = None
        self.file_processor = None

    def get_auth_service(self):
        """
        Returns the authentication service instance. Creates it if it doesn't exist.

        Returns:
            AuthenticationService: Authentication service instance.
        """
        if not self.auth_service:
            self.auth_service = AuthenticationService(self.settings, self.logger)
        return self.auth_service

    def get_sharepoint_service(self):
        """
        Returns the SharePoint service instance. Creates it if it doesn't exist.

        Returns:
            SharePointFolderService: SharePoint service instance.
        """
        if not self.sharepoint_service:
            access_token = self.get_auth_service().get_access_token()
            self.sharepoint_service = SharePointFolderService(
                access_token, self.settings, self.logger
            )
        return self.sharepoint_service

    def get_spreadsheet_service(self):
        """
        Returns the spreadsheet service instance. Creates it if it doesn't exist.

        Returns:
            SpreadsheetService: Spreadsheet service instance.
        """
        if not self.spreadsheet_service:
            self.spreadsheet_service = SpreadsheetService(
                self.settings.columns, self.logger
            )
        return self.spreadsheet_service

    async def get_file_processor(self, session):
        """
        Returns the file processor instance. Creates it if it doesn't exist.

        Args:
            session (aiohttp.ClientSession): HTTP client session.

        Returns:
            FileProcessor: File processor instance.
        """
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
