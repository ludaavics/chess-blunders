import re

import pytest
import requests_mock

from chess_blunders.app.routers.games import CHESSDOTCOM_API_HOST


def test_get_root(client, snapshot):
    response = client.get("/")
    assert response.status_code == 200
    snapshot.assert_match(response.json())


def test_get_games_chessdotcom(client, chessdotcom_username):
    response = client.get(f"/games/chessdotcom/{chessdotcom_username}")
    assert response.status_code == 200


@pytest.mark.flaky(reruns=3)
def test_get_games_chessdotcom_invalid_username(client, chessdotcom_invalid_username):
    response = client.get(f"/games/chessdotcom/{chessdotcom_invalid_username}")
    assert response.status_code == 404


def test_exception_handling(client, chessdotcom_username):
    with requests_mock.Mocker(real_http=True) as m:
        m.get(re.compile(CHESSDOTCOM_API_HOST), status_code=500)
        response = client.get(f"/games/chessdotcom/{chessdotcom_username}")
        assert response.status_code == 503
        assert response.json()["error"]["type"] == "ThirdPartyRequestError"
