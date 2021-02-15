import json
import pathlib
import random

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from chess_blunders.app.api.main import app as api_app


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


# ------------------------------------------------------------------------------------ #
#                                      AWS events                                      #
# ------------------------------------------------------------------------------------ #
def event(name: str):
    name = name if name.endswith(".json") else name + ".json"
    with open(
        pathlib.Path(__file__).parent.absolute().joinpath("fixtures", "api", name)
    ) as f:
        return json.load(f)


@pytest.fixture
def get_games_chessdotcom_event():
    return event("get_games_chessdotcom")


@pytest.fixture
def get_games_chessdotcom_invalid_username_event(get_games_chessdotcom_event):
    event = get_games_chessdotcom_event
    bad_username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=40))
    original_username = event["pathParameters"]["username"]
    return json.loads(
        json.dumps(get_games_chessdotcom_event).replace(original_username, bad_username)
    )


# ------------------------------------------------------------------------------------ #
#                                     AWS contexts                                     #
# ------------------------------------------------------------------------------------ #
@pytest.fixture
def null_context():
    return None
