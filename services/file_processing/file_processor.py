from services.file_processing.file_processing_strategy import FileProcessingStrategy


class FileProcessor:
    def __init__(
        self, session, ws, access_token, drive_id, strategy: FileProcessingStrategy
    ):
        self.session = session
        self.ws = ws
        self.access_token = access_token
        self.drive_id = drive_id
        self.strategy = strategy

    async def process_file(self, file):
        await self.strategy.process(
            file, self.session, self.ws, self.access_token, self.drive_id
        )
