from urllib.parse import quote

from config.logger_config import LoggerConfig
from config.settings import Settings

from ..base.base_service import BaseService


class SharePointFolderService(BaseService):
    """
    Service class for interacting with SharePoint folders.

    Attributes:
        sharepoint_host (str): SharePoint host URL.
        sharepoint_site (str): SharePoint site name.
        logger (Logger): Logger instance.
    """

    def __init__(self, access_token, settings: Settings, logger: LoggerConfig):
        """
        Initializes the SharePointFolderService with access token, settings, and logger.

        Args:
            access_token (str): Access token for authentication.
            settings (Settings): Application settings.
            logger (LoggerConfig): Logger configuration.
        """
        super().__init__(access_token)
        self.sharepoint_host = settings.sharepoint_host
        self.sharepoint_site = settings.sharepoint_site
        self.logger = logger.get_logger(__name__)

    def get_headers(self):
        """
        Returns the headers for the HTTP request.

        Returns:
            dict: Headers for the request.
        """
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

    async def handle_response(self, response):
        """
        Handles the response from the HTTP request.

        Args:
            response (aiohttp.ClientResponse): Response from the request.

        Returns:
            dict: Processed response data.
        """
        if response.status == 200:
            return await response.json()
        else:
            self.logger.error(f"Error making request: {response.status}")
            return None

    async def get_site_id(self):
        """
        Fetches the SharePoint site ID.

        Returns:
            str: SharePoint site ID if found, else None.
        """
        url = f"https://graph.microsoft.com/v1.0/sites/{self.sharepoint_host}:/sites/{self.sharepoint_site}"
        site_data = await self.make_request("GET", url)
        return site_data["id"] if site_data else None

    async def get_drive_id(self, site_id):
        """
        Fetches the drive ID for the specified site ID.

        Args:
            site_id (str): SharePoint site ID.

        Returns:
            str: Drive ID if found, else None.
        """
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
        drives_data = await self.make_request("GET", url)
        if drives_data:
            for drive in drives_data["value"]:
                if drive["name"] == "Documentos":
                    return drive["id"]
            self.logger.error("Drive 'Documentos' not found")
        return None

    async def get_files(self, drive_id, sharepoint_path):
        """
        Fetches the files from the specified SharePoint path.

        Args:
            drive_id (str): Drive ID.
            sharepoint_path (str): Path to the SharePoint folder.

        Returns:
            dict: JSON response containing the files.
        """
        encoded_sharepoint_path = quote(sharepoint_path)
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{encoded_sharepoint_path}:/children"
        return await self.make_request("GET", url)
