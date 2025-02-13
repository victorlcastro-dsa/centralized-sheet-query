import asyncio
import logging

from aiohttp import ClientSession
from openpyxl import Workbook

from auth.authentication import AuthenticationService
from config.settings import Settings
from services.file_processor import process_file
from services.sharepoint_service import SharePointFolderService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    settings = Settings()
    auth_service = AuthenticationService(settings)
    sharepoint_service = SharePointFolderService(
        auth_service.get_access_token(), settings
    )

    async with ClientSession() as session:
        site_id = await sharepoint_service.get_site_id()
        if not site_id:
            return
        logger.info(f"Site ID: {site_id}")

        drive_id = await sharepoint_service.get_drive_id(site_id)
        if not drive_id:
            return
        logger.info(f"Drive ID: {drive_id}")

        files_data = await sharepoint_service.get_files(
            drive_id, settings.sharepoint_path
        )
        files = files_data.get("value", []) if files_data else []

        if not files:
            logger.warning("No files found in the specified SharePoint path")
        else:
            logger.info(f"Found {len(files)} files in the specified SharePoint path")
            for file in files:
                logger.info(f"Found file: {file['name']}")

        wb = Workbook()
        ws = wb.active
        ws.append(["Coluna1", "Coluna2", "Coluna3", "Origem"])
        ws.auto_filter.ref = ws.dimensions

        tasks = [
            process_file(session, file, ws, auth_service.get_access_token(), drive_id)
            for file in files
        ]
        await asyncio.gather(*tasks)

        wb.save("centralizadora.xlsx")
        logger.info("Centralized spreadsheet saved as 'centralizadora.xlsx'")


if __name__ == "__main__":
    asyncio.run(main())
