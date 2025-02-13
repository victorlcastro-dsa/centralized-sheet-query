# config/settings.py
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")
        self.tenant_id = os.getenv("tenant_id")
        self.sharepoint_host = os.getenv("sharepoint_host")
        self.sharepoint_site = os.getenv("sharepoint_site")
        self.sharepoint_path = os.getenv("sharepoint_path")
