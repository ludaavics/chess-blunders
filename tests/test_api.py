import json
import os
import re

import pytest
import requests_mock
from freezegun import freeze_time

from .conftest import aws_events


# ------------------------------------------------------------------------------------ #
#                                         Games                                        #
#                                                                                      #
#                              test_get_games_chessdotcom                              #
#                      test_get_games_chessdotcom_invalid_username                     #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize("event", aws_events("get_games_chessdotcom_events"))
@pytest.mark.flaky(reruns=3)
def test_get_games_chessdotcom(event, null_context):
    from chess_blunders.app.api import handlers

    response = handlers.get_games_chessdotcom(event, null_context)
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
@pytest.mark.parametrize("event", aws_events("request_blunders_events"))
def test_request_blunders(
    event,
    null_context,
    jobs_topic,
    queue,
):
    from chess_blunders.app.api import handlers

    jobs_topic.subscribe(
        Protocol="sqs",
        Endpoint=queue.attributes["QueueArn"],
    )
    response = handlers.request_blunders(event, null_context)
    assert response["statusCode"] == 200

    connection_id = event["requestContext"]["connectionId"]
    messages = queue.receive_messages(MaxNumberOfMessages=1)
    message = json.loads(json.loads(messages[0].body)["Message"])
    assert message["job_name"] == connection_id


@pytest.mark.parametrize("event", aws_events("post_blunders_events"))
def test_post_blunders(event, null_context, jobs_topic_arn):
    from chess_blunders.app.api import handlers

    response = handlers.post_blunders(event, null_context)
    assert response["statusCode"] == 202
    assert "blunders" in response["body"]


@pytest.mark.parametrize("event", aws_events("blunders_job_events"))
def test_blunders_worker(
    event,
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
    response = handlers.blunders_worker(event, null_context)
    snapshot.assert_match(response)

    messages = queue.receive_messages(MaxNumberOfMessages=1)
    enveloppe = json.loads(messages[0].body)
    message = json.loads(enveloppe["Message"])
    message_attributes = enveloppe.get("MessageAttributes", {})
    snapshot.assert_match(message)
    snapshot.assert_match(message_attributes)


@pytest.mark.parametrize("event", aws_events("get_blunders_events"))
def test_get_blunders(event, null_context, blunders_table, snapshot):
    from chess_blunders.app.api import handlers

    response = handlers.get_blunders(event, null_context)
    snapshot.assert_match(response)


# ------------------------------------------------------------------------------------ #
#                                   Publish Blunders                                   #
#                                                                                      #
#                                  test_blunders_to_db                                 #
#                                  test_blunders_to_ws                                 #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize("event", aws_events("blunders_events"))
@freeze_time("2021-01-27")
def test_blunders_to_db(
    event,
    null_context,
    empty_blunders_table,
    snapshot,
):
    from chess_blunders.app.api import handlers

    response = handlers.blunders_to_db(event, null_context)
    response.pop("created_at")
    snapshot.assert_match(response)

    blunders_table = empty_blunders_table
    blunders = blunders_table.scan()
    blunders.pop("ResponseMetadata")  # contains volatile id

    snapshot.assert_match(blunders)


@pytest.mark.skip(reason="Can't mock apigatewaymanagementapi AWS service")
@pytest.mark.parametrize("event", aws_events("blunders_events"))
def test_blunders_to_ws(
    event,
    null_context,
    websocket_api_url,
    snapshot,
):
    from chess_blunders.app.api import handlers

    response = handlers.blunders_to_ws(event, null_context)
    snapshot.assert_match(response)


# ------------------------------------------------------------------------------------ #
#                                 WebSocket Boilerplate                                #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize("event", aws_events("ws_connect_events"))
def test_ws_connect(event, null_context):
    from chess_blunders.app.api import handlers

    response = handlers.ws_connect(event, null_context)
    assert response["statusCode"] == 200


@pytest.mark.parametrize("event", aws_events("ws_disconnect_events"))
def test_ws_disconnect(event, null_context):
    from chess_blunders.app.api import handlers

    response = handlers.ws_disconnect(event, null_context)
    assert response["statusCode"] == 200


@pytest.mark.skip(reason="Can't mock apigatewaymanagementapi AWS service")
@pytest.mark.parametrize("event", aws_events("ws_default_events"))
def test_ws_default(event, null_context):
    from chess_blunders.app.api import handlers

    response = handlers.ws_default(event, null_context)
    assert response["statusCode"] == 200


# ------------------------------------------------------------------------------------ #
#                                      Exceptions                                      #
#                                                                                      #
#                                 test_http_http_error                                 #
#                              test_http_validation_error                              #
#                            test_websocket_validation_error                           #
#                             test_websocket_runtime_error                             #
#                            test_async_queue_runtime_error                            #
# ------------------------------------------------------------------------------------ #
@pytest.mark.parametrize("event", aws_events("get_games_chessdotcom_events"))
def test_http_http_error(event, null_context):
    from chess_blunders.app.api import handlers

    with requests_mock.Mocker(real_http=True) as m:
        m.get(re.compile(handlers.CHESSDOTCOM_API_HOST), status_code=500)
        response = handlers.get_games_chessdotcom(event, null_context)
        assert response["statusCode"] == 503
        assert response["body"]["error"]["type"] == "ThirdPartyRequestError"


@pytest.mark.parametrize("event", aws_events("blunders_events")[:1])
def test_http_validation_error(event, null_context, blunders_table, snapshot):
    from chess_blunders.app.api import handlers

    # NB: this is the wrong event for this route
    response = handlers.get_blunders(event, null_context)
    assert response["statusCode"] == 400
    snapshot.assert_match(response)


@pytest.mark.parametrize("event", aws_events("request_blunders_events")[:1])
def test_websocket_validation_error(event, null_context, caplog):
    from chess_blunders.app.api import handlers

    body = json.loads(event["body"])
    body.pop("username")
    event["body"] = json.dumps(body)

    handlers.request_blunders(event, null_context)
    assert caplog.records
    for record in caplog.records:
        assert "field required" in record.message


@pytest.mark.parametrize("event", aws_events("request_blunders_events")[:1])
def test_websocket_runtime_error(
    event,
    null_context,
    caplog,
):
    from chess_blunders.app.api import handlers

    # NB: we don't have the job_topic fixture, so the below will choke
    response = handlers.request_blunders(event, null_context)

    # the api gateweay should still get a 200 status code ...
    assert response["statusCode"] == 200

    # but we should have an error in the log
    assert caplog.records
    for record in caplog.records:
        assert isinstance(record.msg, KeyError)
        assert record.message == "'JOBS_TOPIC_ARN'"


@pytest.mark.parametrize("event", aws_events("blunders_job_events")[:1])
def test_async_queue_runtime_error(
    event,
    null_context,
    blunders_topic,
    caplog,
):
    from chess_blunders.app.api import handlers

    os.environ["BLUNDERS_TOPIC_ARN"] = "foo"
    handlers.blunders_worker(event, null_context)
    assert caplog.records
    for record in caplog.records:
        assert "Endpoint with arn foo not found" in record.message
