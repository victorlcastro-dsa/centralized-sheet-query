import asyncio
import logging

from app import App

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    app = App()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
