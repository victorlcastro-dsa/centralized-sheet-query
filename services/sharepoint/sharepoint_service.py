from urllib.parse import quote

from config.logger_config import LoggerConfig
from config.settings import Settings

from ..base.base_service import BaseService


class SharePointFolderService(BaseService):
    def __init__(self, access_token, settings: Settings, logger: LoggerConfig):
        super().__init__(access_token)
        self.sharepoint_host = settings.sharepoint_host
        self.sharepoint_site = settings.sharepoint_site
        self.logger = logger.get_logger(__name__)

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

    async def handle_response(self, response):
        if response.status == 200:
            return await response.json()
        else:
            self.logger.error(f"Error making request: {response.status}")
            return None

    async def get_site_id(self):
        url = f"https://graph.microsoft.com/v1.0/sites/{self.sharepoint_host}:/sites/{self.sharepoint_site}"
        site_data = await self.make_request("GET", url)
        return site_data["id"] if site_data else None

    async def get_drive_id(self, site_id):
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        drives_data = await self.make_request("GET", url)
        if drives_data:
            for drive in drives_data["value"]:
                if drive["name"] == "Documentos":
                    return drive["id"]
            self.logger.error("Drive 'Documentos' not found")
        return None

    async def get_files(self, drive_id, sharepoint_path):
        encoded_sharepoint_path = quote(sharepoint_path)
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{encoded_sharepoint_path}:/children"
        return await self.make_request("GET", url)
