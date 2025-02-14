import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Settings class to load and store application configuration from environment variables.

    Attributes:
        client_id (str): Client ID for authentication.
        client_secret (str): Client secret for authentication.
        tenant_id (str): Tenant ID for authentication.
        sharepoint_host (str): SharePoint host URL.
        sharepoint_site (str): SharePoint site name.
        sharepoint_path (str): Path to the SharePoint folder.
        columns (List[str]): List of column names for the spreadsheet.
        output_filename (str): Name of the output file.
        origin_column_name (str): Name of the origin column.
        log_level (str): Logging level.
    """

    def __init__(self) -> None:
        """
        Initializes the Settings class by loading environment variables.
        """
        self.client_id: str = os.getenv("client_id", "")
        self.client_secret: str = os.getenv("client_secret", "")
        self.tenant_id: str = os.getenv("tenant_id", "")
        self.sharepoint_host: str = os.getenv("sharepoint_host", "")
        self.sharepoint_site: str = os.getenv("sharepoint_site", "")
        self.sharepoint_path: str = os.getenv("sharepoint_path", "")
        self.columns: List[str] = os.getenv("columns", "").split(",")
        self.output_filename: str = os.getenv("output_filename", "consolidated.xlsx")
        self.origin_column_name: str = os.getenv("origin_column_name", "Origem")
        self.log_level: str = os.getenv("log_level", "INFO")
