import random

import pytest
from fastapi.testclient import TestClient

from chess_blunders import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture()
def chessdotcom_username():
    return "hikaru"


@pytest.fixture()
def chessdotcom_invalid_username():
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=40))
