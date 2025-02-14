from io import BytesIO

import pandas as pd

from config.logger_config import LoggerConfig
from services.file_processing.file_processing_strategy import FileProcessingStrategy

logger = LoggerConfig.get_logger(__name__)


class ExcelProcessingStrategy(FileProcessingStrategy):
    async def process(self, file, session, ws, access_token, drive_id):
        if file["name"].endswith(".xlsx"):
            file_id = file["id"]
            logger.info(f"Processing file: {file['name']}")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}/content"
            async with session.get(url, headers=headers) as file_response:
                if file_response.status == 200:
                    excel_data = BytesIO(await file_response.read())
                    df = pd.read_excel(excel_data)
                    if not df.empty:
                        for row in df.itertuples(index=False, name=None):
                            ws.append(row + (file["name"],))
                        logger.info(f"File {file['name']} processed successfully")
                    else:
                        logger.warning(f"File {file['name']} is empty")
                else:
                    logger.error(
                        f"Error downloading file {file['name']}: {file_response.status}"
                    )
                    logger.error(f"Response: {await file_response.text()}")
