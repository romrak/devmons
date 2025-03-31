import asyncio
import logging

import uvicorn

from crypkit.config import Config
from crypkit.container import CrypkitContainer

container = CrypkitContainer()
container.config.from_pydantic(Config())

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


async def background_task() -> None:
    while True:
        await container.crypto_service().refresh()
        await asyncio.sleep(3600)


async def main() -> None:
    task = asyncio.create_task(background_task())

    config = uvicorn.Config(
        "crypkit.adapters.api.app:app",
        host="0.0.0.0",  # noqa: S104
    )
    server = uvicorn.Server(config)

    try:
        await server.serve()
    finally:
        task.cancel()
        await task


if __name__ == "__main__":
    asyncio.run(main())
