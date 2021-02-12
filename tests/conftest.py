import json
import pathlib
import random

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from chess_blunders.app.api import app as api_app


@pytest.fixture(scope="session")
def api_client():
    return TestClient(api_app)


@pytest.fixture()
async def async_api_client():
    async with AsyncClient(app=api_app, base_url="http://test") as client:
        yield client


@pytest.fixture()
def chessdotcom_username():
    return "hikaru"


@pytest.fixture()
def chessdotcom_invalid_username():
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=40))


@pytest.fixture()
def games():
    with open(pathlib.Path(__file__).parent.absolute() / "fixtures/games.json") as f:
        return json.load(f)
