import time

import msal

from config.logger_config import LoggerConfig
from config.settings import Settings


class AuthenticationService:
    def __init__(self, settings: Settings, logger: LoggerConfig):
        self.client_id = settings.client_id
        self.client_secret = settings.client_secret
        self.tenant_id = settings.tenant_id
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.access_token = None
        self.token_expires_at = 0
        self.logger = logger.get_logger(__name__)
        self._authenticate()

    def _authenticate(self):
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )
        result = app.acquire_token_for_client(scopes=self.scope)
        if "access_token" in result:
            self.access_token = result["access_token"]
            self.token_expires_at = time.time() + result["expires_in"]
            self.logger.info("Access token obtained successfully")
        else:
            self.logger.error("Error obtaining access token")
            exit()

    def get_access_token(self):
        if time.time() >= self.token_expires_at:
            self.logger.info("Access token expired, re-authenticating...")
            self._authenticate()
        return self.access_token
