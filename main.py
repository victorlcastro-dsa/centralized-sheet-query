import asyncio

from app.app import App
from config.logger_config import LoggerConfig
from config.settings import Settings
from services.factory.service_factory import ServiceFactory

LoggerConfig.setup_logging()


async def main():
    """
    Main entry point of the application. Initializes settings, logger, service factory,
    and the main application class, then runs the application.
    """
    settings = Settings()
    logger = LoggerConfig()
    factory = ServiceFactory(settings, logger)
    app = App(settings, logger, factory)
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
