import time
from typing import List

import msal

from config.logger_config import LoggerConfig
from config.settings import Settings


class AuthenticationService:
    """
    Authentication service to obtain access tokens from Microsoft Graph API.

    Attributes:
        client_id (str): Client ID.
        client_secret (str): Client secret.
        tenant_id (str): Tenant ID.
        authority (str): Authority URL for authentication.
        scope (List[str]): Scope of permissions for the token.
        access_token (str): Access token.
        token_expires_at (float): Token expiration timestamp.
        logger (Logger): Logger instance.
    """

    def __init__(self, settings: Settings, logger: LoggerConfig) -> None:
        """
        Initializes the AuthenticationService class with settings and logger.

        Args:
            settings (Settings): Application settings.
            logger (LoggerConfig): Logger configuration.
        """
        self.client_id: str = settings.client_id
        self.client_secret: str = settings.client_secret
        self.tenant_id: str = settings.tenant_id
        self.authority: str = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope: List[str] = ["https://graph.microsoft.com/.default"]
        self.access_token: str = ""
        self.token_expires_at: float = 0
        self.logger = logger.get_logger(__name__)
        self._authenticate()

    def _authenticate(self) -> None:
        """
        Authenticates the client and obtains an access token.
        """
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

    def get_access_token(self) -> str:
        """
        Returns the access token. Re-authenticates if the token has expired.

        Returns:
            str: Access token.
        """
        if time.time() >= self.token_expires_at:
            self.logger.info("Access token expired, re-authenticating...")
            self._authenticate()
        return self.access_token
