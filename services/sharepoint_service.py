import logging
from urllib.parse import quote

from .base_service import BaseService

logger = logging.getLogger(__name__)


class SharePointFolderService(BaseService):
    def __init__(self, access_token, settings):
        super().__init__(access_token)
        self.sharepoint_host = settings.sharepoint_host
        self.sharepoint_site = settings.sharepoint_site

    async def get_site_id(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
        url = f"https://graph.microsoft.com/v1.0/sites/{self.sharepoint_host}:/sites/{self.sharepoint_site}"
        site_data = await self.make_request("GET", url, headers=headers)
        return site_data["id"] if site_data else None

    async def get_drive_id(self, site_id):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        drives_data = await self.make_request("GET", url, headers=headers)
        if drives_data:
            for drive in drives_data["value"]:
                if drive["name"] == "Documentos":
                    return drive["id"]
            logger.error("Drive 'Documentos' not found")
        return None

    async def get_files(self, drive_id, sharepoint_path):
        encoded_sharepoint_path = quote(sharepoint_path)
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{encoded_sharepoint_path}:/children"
        return await self.make_request("GET", url, headers=headers)
