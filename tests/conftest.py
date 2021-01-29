import random

import pytest
from fastapi.testclient import TestClient

from chess_blunders.api import app as api_app


@pytest.fixture(scope="session")
def api_client():
    return TestClient(api_app)


@pytest.fixture()
def chessdotcom_username():
    return "hikaru"


@pytest.fixture()
def chessdotcom_invalid_username():
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=40))
