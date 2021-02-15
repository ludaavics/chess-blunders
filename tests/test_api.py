import re

import pytest
import requests_mock

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
#                                  test_post_blunders                                  #
# ------------------------------------------------------------------------------------ #
def test_post_blunders(post_blunders_event, null_context, snapshot):
    response = handlers.post_blunders(post_blunders_event, null_context)
    snapshot.assert_match(response)


# ------------------------------------------------------------------------------------ #
#                                      Exceptions                                      #
#                                                                                      #
#                                test_exception_handling                               #
# ------------------------------------------------------------------------------------ #
def test_exception_handling(get_games_chessdotcom_event, null_context):
    with requests_mock.Mocker(real_http=True) as m:
        m.get(re.compile(handlers.CHESSDOTCOM_API_HOST), status_code=500)
        response = handlers.get_games_chessdotcom(
            get_games_chessdotcom_event, null_context
        )
        assert response["statusCode"] == 503
        assert response["body"]["error"]["type"] == "ThirdPartyRequestError"
