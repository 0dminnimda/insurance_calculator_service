"""
Things that simplify the testing process and help with it
"""

from __future__ import annotations

import random
from typing import Iterator

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from insurance_calculator_service import app, options


def setup():
    random.seed(69)
    options.DEV_MODE = True


### pytest ###


@pytest.fixture()
async def client() -> Iterator[AsyncClient]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c


@pytest.fixture()
def anyio_backend():
    return "asyncio"


def do_test(file: str) -> None:
    pytest.main([file, "-vv", "-W", "ignore::pytest.PytestAssertRewriteWarning"])
