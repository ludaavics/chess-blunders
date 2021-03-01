import json
import re

import pytest
import requests_mock

from .conftest import aws_events


# ------------------------------------------------------------------------------------ #
#                                         Games                                        #
#                                                                                      #
#                              test_get_games_chessdotcom                              #
#                      test_get_games_chessdotcom_invalid_username                     #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize(
    "get_games_chessdotcom_event", aws_events("get_games_chessdotcom_events")
)
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
#                                    Create Blunders                                   #
#                                                                                      #
#                                 test_request_blunders                                #
#                                  test_post_blunders                                  #
#                                 test_blunders_worker                                 #
#                                   test_get_blunders                                  #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize(
    "request_blunders_event", aws_events("request_blunders_events")
)
def test_request_blunders(
    request_blunders_event,
    null_context,
    jobs_topic,
    queue,
):
    from chess_blunders.app.api import handlers

    jobs_topic.subscribe(
        Protocol="sqs",
        Endpoint=queue.attributes["QueueArn"],
    )
    response = handlers.request_blunders(request_blunders_event, null_context)
    assert response["statusCode"] == 200

    connection_id = request_blunders_event["requestContext"]["connectionId"]
    messages = queue.receive_messages(MaxNumberOfMessages=1)
    message = json.loads(json.loads(messages[0].body)["Message"])
    assert message["job_name"] == connection_id


@pytest.mark.parametrize("post_blunders_event", aws_events("post_blunders_events"))
def test_post_blunders(post_blunders_event, null_context, jobs_topic_arn):
    from chess_blunders.app.api import handlers

    response = handlers.post_blunders(post_blunders_event, null_context)
    assert response["statusCode"] == 202
    assert "blunders" in response["body"]


@pytest.mark.parametrize("blunders_job_event", aws_events("blunders_job_events"))
def test_blunders_worker(
    blunders_job_event,
    null_context,
    blunders_topic,
    queue,
    snapshot,
):
    from chess_blunders.app.api import handlers

    blunders_topic.subscribe(
        Protocol="sqs",
        Endpoint=queue.attributes["QueueArn"],
    )
    response = handlers.blunders_worker(blunders_job_event, null_context)
    snapshot.assert_match(response)

    messages = queue.receive_messages(MaxNumberOfMessages=1)
    enveloppe = json.loads(messages[0].body)
    message = json.loads(enveloppe["Message"])
    message_attributes = enveloppe["MessageAttributes"]
    snapshot.assert_match(message)
    snapshot.assert_match(message_attributes)


@pytest.mark.parametrize("blunders_event", aws_events("blunders_events"))
def test_get_blunders(blunders_event, null_context, blunders_table, snapshot):
    from chess_blunders.app.api import handlers

    response = handlers.get_blunders(blunders_event, null_context)
    snapshot.assert_match(response)


# ------------------------------------------------------------------------------------ #
#                                   Publish Blunders                                   #
#                                                                                      #
#                                  test_blunders_to_db                                 #
#                                  test_blunders_to_ws                                 #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize("blunders_event", aws_events("blunders_events"))
def test_blunders_to_db(
    blunders_event,
    null_context,
    empty_blunders_table,
    snapshot,
):
    from chess_blunders.app.api import handlers

    response = handlers.blunders_to_db(blunders_event, null_context)
    response.pop("created_at")
    snapshot.assert_match(response)

    blunders_table = empty_blunders_table
    blunders = blunders_table.scan()

    snapshot.assert_match(blunders)


@pytest.mark.skip(reason="Can't mock apigatewaymanagementapi AWS service")
@pytest.mark.parametrize("blunders_event", aws_events("blunders_events"))
def test_blunders_to_ws(
    blunders_event,
    null_context,
    websocket_api_url,
    snapshot,
):
    from chess_blunders.app.api import handlers

    response = handlers.blunders_to_ws(blunders_event, null_context)
    snapshot.assert_match(response)


# ------------------------------------------------------------------------------------ #
#                                      Exceptions                                      #
#                                                                                      #
#                                test_exception_handling                               #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize(
    "get_games_chessdotcom_event", aws_events("get_games_chessdotcom_events")
)
def test_exception_handling(get_games_chessdotcom_event, null_context):
    from chess_blunders.app.api import handlers

    with requests_mock.Mocker(real_http=True) as m:
        m.get(re.compile(handlers.CHESSDOTCOM_API_HOST), status_code=500)
        response = handlers.get_games_chessdotcom(
            get_games_chessdotcom_event, null_context
        )
        assert response["statusCode"] == 503
        assert response["body"]["error"]["type"] == "ThirdPartyRequestError"
