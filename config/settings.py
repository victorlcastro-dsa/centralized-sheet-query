import os

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
        columns (list): List of column names for the spreadsheet.
        output_filename (str): Name of the output file.
        origin_column_name (str): Name of the origin column.
        log_level (str): Logging level.
    """

    def __init__(self):
        """
        Initializes the Settings class by loading environment variables.
        """
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")
        self.tenant_id = os.getenv("tenant_id")
        self.sharepoint_host = os.getenv("sharepoint_host")
        self.sharepoint_site = os.getenv("sharepoint_site")
        self.sharepoint_path = os.getenv("sharepoint_path")
        self.columns = os.getenv("columns").split(",")
        self.output_filename = os.getenv("output_filename", "consolidated.xlsx")
        self.origin_column_name = os.getenv("origin_column_name", "Origem")
        self.log_level = os.getenv("log_level", "INFO")
