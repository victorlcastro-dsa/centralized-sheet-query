from io import BytesIO

import pandas as pd

from config.logger_config import LoggerConfig

logger = LoggerConfig.get_logger(__name__)


class FileProcessor:
    def __init__(self, session, ws, access_token, drive_id):
        self.session = session
        self.ws = ws
        self.access_token = access_token
        self.drive_id = drive_id

    async def process_file(self, file):
        if file["name"].endswith(".xlsx"):
            file_id = file["id"]
            logger.info(f"Processing file: {file['name']}")
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json",
            }
            url = f"https://graph.microsoft.com/v1.0/drives/{self.drive_id}/items/{file_id}/content"
            async with self.session.get(url, headers=headers) as file_response:
                if file_response.status == 200:
                    excel_data = BytesIO(await file_response.read())
                    df = pd.read_excel(excel_data)
                    if not df.empty:
                        for row in df.itertuples(index=False, name=None):
                            self.ws.append(row + (file["name"],))
                        logger.info(f"File {file['name']} processed successfully")
                    else:
                        logger.warning(f"File {file['name']} is empty")
                else:
                    logger.error(
                        f"Error downloading file {file['name']}: {file_response.status}"
                    )
                    logger.error(f"Response: {await file_response.text()}")
