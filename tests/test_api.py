import re

import pytest
import requests_mock

from chess_blunders.api.routers.games import CHESSDOTCOM_API_HOST


@pytest.mark.asyncio
async def test_get_root(async_api_client, snapshot):
    response = await async_api_client.get("/")
    assert response.status_code == 200
    snapshot.assert_match(response.json())


# ------------------------------------------------------------------------------------ #
#                                         Games                                        #
#                                                                                      #
#                              test_get_games_chessdotcom                              #
#                      test_get_games_chessdotcom_invalid_username                     #
# ------------------------------------------------------------------------------------ #
def test_get_games_chessdotcom(api_client, chessdotcom_username):
    response = api_client.get(f"/games/chessdotcom/{chessdotcom_username}")
    assert response.status_code == 200


@pytest.mark.flaky(reruns=3)
def test_get_games_chessdotcom_invalid_username(
    api_client, chessdotcom_invalid_username
):
    response = api_client.get(f"/games/chessdotcom/{chessdotcom_invalid_username}")
    assert response.status_code == 404


# ------------------------------------------------------------------------------------ #
#                                        Puzzles                                       #
#                                                                                      #
#                              test_create_blunder_puzzles                             #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize("games_loc", [slice(None, 1), slice(1, 3)])
@pytest.mark.asyncio
async def test_create_blunder_puzzles(async_api_client, games, games_loc, snapshot):
    payload = {"games": games[games_loc]}
    response = await async_api_client.post("/puzzles/blunders", json=payload)
    assert response.status_code == 201
    snapshot.assert_match(response.json())


# ------------------------------------------------------------------------------------ #
#                                      Exceptions                                      #
#                                                                                      #
#                                test_exception_handling                               #
# ------------------------------------------------------------------------------------ #
def test_exception_handling(api_client, chessdotcom_username):
    with requests_mock.Mocker(real_http=True) as m:
        m.get(re.compile(CHESSDOTCOM_API_HOST), status_code=500)
        response = api_client.get(f"/games/chessdotcom/{chessdotcom_username}")
        assert response.status_code == 503
        assert response.json()["error"]["type"] == "ThirdPartyRequestError"
