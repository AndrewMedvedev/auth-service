import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.schemas import IdentityProviderSchema
from src.database.repository import IdentityRepository


async def main() -> None:
    yandex = IdentityProviderSchema(
        name="Yandex", type="oauth", scopes=["login:info ", "login:email"]
    )
    await IdentityRepository().create(schema=yandex)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
