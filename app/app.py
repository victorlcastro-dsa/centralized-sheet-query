import asyncio
from typing import Any, Dict, List

from aiohttp import ClientSession

from config.logger_config import LoggerConfig
from config.settings import Settings
from services.factory.service_factory import ServiceFactory

logger = LoggerConfig.get_logger(__name__)


class App:
    """
    Main application class that orchestrates the process of fetching and processing
    files from SharePoint and generating a centralized spreadsheet.

    Attributes:
        factory (ServiceFactory): Service factory to obtain service instances.
        auth_service (AuthenticationService): Authentication service.
        sharepoint_service (SharePointFolderService): Service to interact with SharePoint.
        spreadsheet_service (SpreadsheetService): Service for spreadsheet manipulation.
    """

    def __init__(
        self, settings: Settings, logger: LoggerConfig, factory: ServiceFactory
    ) -> None:
        """
        Initializes the App class with settings, logger, and service factory.

        Args:
            settings (Settings): Application settings.
            logger (LoggerConfig): Logger configuration.
            factory (ServiceFactory): Service factory.
        """
        self.factory: ServiceFactory = factory
        self.auth_service = self.factory.get_auth_service()
        self.sharepoint_service = self.factory.get_sharepoint_service()
        self.spreadsheet_service = self.factory.get_spreadsheet_service()

    async def run(self) -> None:
        """
        Executes the main process of the application, which includes:
        - Fetching the SharePoint site ID.
        - Fetching the SharePoint drive ID.
        - Fetching files from SharePoint.
        - Processing the fetched files.
        - Saving the centralized spreadsheet.
        """
        async with ClientSession() as session:
            site_id: str = await self.sharepoint_service.get_site_id()
            if not site_id:
                return
            logger.info(f"Site ID: {site_id}")

            drive_id: str = await self.sharepoint_service.get_drive_id(site_id)
            if not drive_id:
                return
            logger.info(f"Drive ID: {drive_id}")

            files_data: Dict[str, Any] = await self.sharepoint_service.get_files(
                drive_id, self.factory.settings.sharepoint_path
            )
            files: List[Dict[str, Any]] = (
                files_data.get("value", []) if files_data else []
            )

            if not files:
                logger.warning("No files found in the specified SharePoint path")
            else:
                logger.info(
                    f"Found {len(files)} files in the specified SharePoint path"
                )
                for file in files:
                    logger.info(f"Found file: {file['name']}")

            file_processor = await self.factory.get_file_processor(session)
            tasks = [file_processor.process_file(file) for file in files]
            await asyncio.gather(*tasks)

            self.spreadsheet_service.save(self.factory.settings.output_filename)
