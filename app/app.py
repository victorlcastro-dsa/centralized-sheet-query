import asyncio

from aiohttp import ClientSession

from config.logger_config import LoggerConfig
from config.settings import Settings
from services.factory.service_factory import ServiceFactory

logger = LoggerConfig.get_logger(__name__)


class App:
    def __init__(
        self, settings: Settings, logger: LoggerConfig, factory: ServiceFactory
    ):
        self.factory = factory
        self.auth_service = self.factory.get_auth_service()
        self.sharepoint_service = self.factory.get_sharepoint_service()
        self.spreadsheet_service = self.factory.get_spreadsheet_service()

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
                drive_id, self.factory.settings.sharepoint_path
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

            file_processor = await self.factory.get_file_processor(session)
            tasks = [file_processor.process_file(file) for file in files]
            await asyncio.gather(*tasks)

            self.spreadsheet_service.save("centralizadora.xlsx")
