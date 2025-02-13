import asyncio

from app import App
from config.logger_config import LoggerConfig

LoggerConfig.setup_logging()


async def main():
    app = App()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
