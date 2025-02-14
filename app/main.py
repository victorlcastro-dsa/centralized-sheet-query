import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import App
from config.logger_config import LoggerConfig
from config.settings import Settings

LoggerConfig.setup_logging()


async def main():
    settings = Settings()
    logger = LoggerConfig()
    app = App(settings, logger)
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
