import asyncio

from aiohttp import ClientSession

from auth.authentication import AuthenticationService
from config.logger_config import LoggerConfig
from config.settings import Settings
from services.file_processor import FileProcessor
from services.sharepoint_service import SharePointFolderService
from services.spreadsheet_service import SpreadsheetService

logger = LoggerConfig.get_logger(__name__)


class App:
    def __init__(self):
        self.settings = Settings()
        self.auth_service = AuthenticationService(self.settings)
        self.sharepoint_service = SharePointFolderService(
            self.auth_service.get_access_token(), self.settings
        )
        self.spreadsheet_service = SpreadsheetService(self.settings.columns)

    async def run(self):
        async with ClientSession() as session:
            site_id = await self.sharepoint_service.get_site_id()
            if not site_id:
                return
            logger.info(f"Site ID: {site_id}")

            drive_id = await self.sharepoint_service.get_drive_id(site_id)
            if not drive_id:
                return
            logger.info(f"Drive ID: {drive_id}")

            files_data = await self.sharepoint_service.get_files(
                drive_id, self.settings.sharepoint_path
            )
            files = files_data.get("value", []) if files_data else []

            if not files:
                logger.warning("No files found in the specified SharePoint path")
            else:
                logger.info(
                    f"Found {len(files)} files in the specified SharePoint path"
                )
                for file in files:
                    logger.info(f"Found file: {file['name']}")

            file_processor = FileProcessor(
                session,
                self.spreadsheet_service.ws,
                self.auth_service.get_access_token(),
                drive_id,
            )
            tasks = [file_processor.process_file(file) for file in files]
            await asyncio.gather(*tasks)

            self.spreadsheet_service.save("centralizadora.xlsx")
