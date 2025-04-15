import asyncio
from typing import Any

import aiohttp
import pytest_asyncio

pytest_plugins = (
    "fixtures.table_fixtures",
    "fixtures.reservation_fixtures",
    "fixtures.db_fixtures",
)


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client_session() -> aiohttp.ClientSession:
    client_session = aiohttp.ClientSession()
    yield client_session
    await client_session.close()


@pytest_asyncio.fixture(scope="session")
async def make_request(client_session):
    async def inner(endpoint: str, method: str = "GET", data: dict | None = None) -> tuple[Any, Any]:
        data: dict = data or {}
        async with client_session.request(
                method,
                endpoint,
                data=data,
                headers={"Content-Type": "application/json"}
        ) as raw_response:
            response = await raw_response.json()
            status = raw_response.status

            return status, response

    return inner
