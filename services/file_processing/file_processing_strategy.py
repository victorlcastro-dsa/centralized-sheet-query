from abc import ABC, abstractmethod


class FileProcessingStrategy(ABC):
    @abstractmethod
    async def process(self, file, session, ws, access_token, drive_id):
        pass
