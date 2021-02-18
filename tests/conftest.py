import json
import pathlib
import random

import pytest


@pytest.fixture()
def games():
    with open(
        pathlib.Path(__file__).parent.absolute() / "fixtures/core/games.json"
    ) as f:
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
    return event("get_games_chessdotcom_event")


@pytest.fixture
def get_games_chessdotcom_invalid_username_event(get_games_chessdotcom_event):
    event = get_games_chessdotcom_event
    bad_username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=40))
    original_username = event["pathParameters"]["username"]
    return json.loads(
        json.dumps(get_games_chessdotcom_event).replace(original_username, bad_username)
    )


@pytest.fixture
def get_games_chessdotcom_invalid_query_params_event(get_games_chessdotcom_event):
    event = get_games_chessdotcom_event
    event["queryStringParameters"] = {"limit": -1}
    return event


@pytest.fixture()
def post_blunders_events():
    return event("post_blunders_events")


# ------------------------------------------------------------------------------------ #
#                                     AWS contexts                                     #
# ------------------------------------------------------------------------------------ #
@pytest.fixture
def null_context():
    return None
