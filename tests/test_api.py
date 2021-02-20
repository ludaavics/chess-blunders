import re

import pytest
import requests_mock


# ------------------------------------------------------------------------------------ #
#                                         Games                                        #
#                                                                                      #
#                              test_get_games_chessdotcom                              #
#                      test_get_games_chessdotcom_invalid_username                     #
# ------------------------------------------------------------------------------------ #
def test_get_games_chessdotcom(get_games_chessdotcom_event, null_context):
    from chess_blunders.app.api import handlers

    response = handlers.get_games_chessdotcom(get_games_chessdotcom_event, null_context)
    assert response["statusCode"] == 200


@pytest.mark.flaky(reruns=3)
def test_get_games_chessdotcom_invalid_username(
    get_games_chessdotcom_invalid_username_event, null_context
):
    from chess_blunders.app.api import handlers

    response = handlers.get_games_chessdotcom(
        get_games_chessdotcom_invalid_username_event, null_context
    )
    assert response["statusCode"] == 404


def test_get_games_chessdotcom_invalid_query_params(
    get_games_chessdotcom_invalid_query_params_event, null_context, snapshot
):
    from chess_blunders.app.api import handlers

    response = handlers.get_games_chessdotcom(
        get_games_chessdotcom_invalid_query_params_event, null_context
    )
    snapshot.assert_match(response)


# ------------------------------------------------------------------------------------ #
#                                       Blunders                                       #
#                                                                                      #
#                                  test_post_blunders                                  #
# ------------------------------------------------------------------------------------ #
def test_post_blunders(post_blunders_events, null_context, jobs_topic):
    from chess_blunders.app.api import handlers

    for post_blunders_event in post_blunders_events:
        response = handlers.post_blunders(post_blunders_event, null_context)
        assert response["statusCode"] == 202
        assert "blunders" in response["body"]


def test_blunders_worker(
    blunders_worker_sns_events, null_context, blunders_table, snapshot
):
    from chess_blunders.app.api import handlers

    for sns_event in blunders_worker_sns_events:
        response = handlers.blunders_worker(sns_event, null_context)
        snapshot.assert_match(response)


# ------------------------------------------------------------------------------------ #
#                                      Exceptions                                      #
#                                                                                      #
#                                test_exception_handling                               #
# ------------------------------------------------------------------------------------ #
def test_exception_handling(get_games_chessdotcom_event, null_context):
    from chess_blunders.app.api import handlers

    with requests_mock.Mocker(real_http=True) as m:
        m.get(re.compile(handlers.CHESSDOTCOM_API_HOST), status_code=500)
        response = handlers.get_games_chessdotcom(
            get_games_chessdotcom_event, null_context
        )
        assert response["statusCode"] == 503
        assert response["body"]["error"]["type"] == "ThirdPartyRequestError"
