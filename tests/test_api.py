import pytest

from chess_blunders.app.api import handlers


# ------------------------------------------------------------------------------------ #
#                                         Games                                        #
#                                                                                      #
#                              test_get_games_chessdotcom                              #
#                      test_get_games_chessdotcom_invalid_username                     #
# ------------------------------------------------------------------------------------ #
def test_get_games_chessdotcom(get_games_chessdotcom_event, null_context):
    response = handlers.get_games_chessdotcom(get_games_chessdotcom_event, null_context)
    assert response["statusCode"] == 200


@pytest.mark.flaky(reruns=3)
def test_get_games_chessdotcom_invalid_username(
    get_games_chessdotcom_invalid_username_event, null_context
):
    response = handlers.get_games_chessdotcom(
        get_games_chessdotcom_invalid_username_event, null_context
    )
    assert response["statusCode"] == 404


# ------------------------------------------------------------------------------------ #
#                                        Puzzles                                       #
#                                                                                      #
#                              test_create_blunder_puzzles                             #
# ------------------------------------------------------------------------------------ #
# @pytest.mark.parametrize(
#     "games_loc,colors", [(slice(None, 1), None), (slice(1, 3), ["white", "black"])]
# )
# @pytest.mark.asyncio
# async def test_create_blunder_puzzles(
#     async_api_client, games, games_loc, colors, snapshot
# ):
#     payload = {"games": games[games_loc], "colors": colors}
#     response = await async_api_client.post("/puzzles/blunders", json=payload)
#     assert response.status_code == 201
#     snapshot.assert_match(response.json())


# ------------------------------------------------------------------------------------ #
#                                      Exceptions                                      #
#                                                                                      #
#                                test_exception_handling                               #
# ------------------------------------------------------------------------------------ #
# def test_exception_handling(api_client, chessdotcom_username):
#     with requests_mock.Mocker(real_http=True) as m:
#         m.get(re.compile(CHESSDOTCOM_API_HOST), status_code=500)
#         response = api_client.get(f"/games/chessdotcom/{chessdotcom_username}")
#         assert response.status_code == 503
#         assert response.json()["error"]["type"] == "ThirdPartyRequestError"
