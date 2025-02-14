from auth.authentication import AuthenticationService
from config.settings import Settings
from services.file_processor import FileProcessor
from services.sharepoint_service import SharePointFolderService
from services.spreadsheet_service import SpreadsheetService


class ServiceFactory:
    def __init__(self):
        self.settings = Settings()
        self.auth_service = None
        self.sharepoint_service = None
        self.spreadsheet_service = None
        self.file_processor = None

    def get_auth_service(self):
        if not self.auth_service:
            self.auth_service = AuthenticationService(self.settings)
        return self.auth_service

    def get_sharepoint_service(self):
        if not self.sharepoint_service:
            access_token = self.get_auth_service().get_access_token()
            self.sharepoint_service = SharePointFolderService(
                access_token, self.settings
            )
        return self.sharepoint_service

    def get_spreadsheet_service(self):
        if not self.spreadsheet_service:
            self.spreadsheet_service = SpreadsheetService(self.settings.columns)
        return self.spreadsheet_service

    async def get_file_processor(self, session):
        if not self.file_processor:
            self.file_processor = FileProcessor(
                session,
                self.get_spreadsheet_service().ws,
                self.get_auth_service().get_access_token(),
                await self.get_sharepoint_service().get_drive_id(
                    await self.get_sharepoint_service().get_site_id()
                ),
            )
        return self.file_processor
