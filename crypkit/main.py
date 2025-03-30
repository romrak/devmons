import uvicorn

from crypkit.config import Config
from crypkit.container import CrypkitContainer

container = CrypkitContainer()
container.config.from_pydantic(Config())


def main() -> None:
    uvicorn.run(
        "crypkit.adapters.api.app:app",
        host="0.0.0.0",  # noqa: S104
    )


if __name__ == "__main__":
    main()
