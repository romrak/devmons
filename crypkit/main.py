import logging

import uvicorn

from crypkit.config import Config
from crypkit.container import CrypkitContainer

container = CrypkitContainer()
container.config.from_pydantic(Config())

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def main() -> None:
    uvicorn.run(
        "crypkit.adapters.api.app:app",
        host="0.0.0.0",  # noqa: S104
    )


if __name__ == "__main__":
    main()
