import pandas as pd

from config.logger_config import LoggerConfig
from services.file_processing.strategies.base_file_processing_strategy import (
    BaseFileProcessingStrategy,
)

logger = LoggerConfig.get_logger(__name__)


class ExcelProcessingStrategy(BaseFileProcessingStrategy):
    def __init__(self):
        super().__init__(".xlsx")

    async def process_content(self, file_content, file, ws):
        df = pd.read_excel(file_content)
        if not df.empty:
            for row in df.itertuples(index=False, name=None):
                ws.append(row + (file["name"],))
            logger.info(f"File {file['name']} processed successfully")
        else:
            logger.warning(f"File {file['name']} is empty")
