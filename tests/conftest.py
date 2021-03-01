import json
import os
import pathlib
import random

import boto3
import moto
import pytest


@pytest.fixture
def games():
    with open(
        pathlib.Path(__file__).parent.absolute() / "fixtures/core/games.json"
    ) as f:
        return json.load(f)


# ------------------------------------------------------------------------------------ #
#                                  Mock AWS Resources                                  #
# ------------------------------------------------------------------------------------ #
# ------------------------------------ Credentials ----------------------------------- #
@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


# ---------------------------------------- SNS --------------------------------------- #
@pytest.fixture
def sns(aws_credentials):
    with moto.mock_sns():
        yield boto3.resource("sns")


@pytest.fixture
def jobs_topic_arn(sns):
    original = os.getenv("JOBS_TOPIC_ARN")

    topic = sns.create_topic(Name="test-jobs-topic")
    os.environ["JOBS_TOPIC_ARN"] = topic.attributes["TopicArn"]
    yield topic.attributes["TopicArn"]
    if original is None:
        os.environ.pop("JOBS_TOPIC_ARN")
    else:
        os.environ["JOBS_TOPIC_ARN"] = original


@pytest.fixture
def jobs_topic(sns, jobs_topic_arn):
    yield sns.Topic(jobs_topic_arn)


@pytest.fixture
def blunders_topic_arn(sns):
    original = os.getenv("BLUNDERS_TOPIC_ARN")

    topic = sns.create_topic(Name="test-blunders-topic")
    os.environ["BLUNDERS_TOPIC_ARN"] = topic.attributes["TopicArn"]
    yield topic.attributes["TopicArn"]
    if original is None:
        os.environ.pop("BLUNDERS_TOPIC_ARN")
    else:
        os.environ["BLUNDERS_TOPIC_ARN"] = original


@pytest.fixture
def blunders_topic(sns, blunders_topic_arn):
    yield sns.Topic(blunders_topic_arn)


# ---------------------------------------- SQS --------------------------------------- #
@pytest.fixture
def sqs(aws_credentials):
    with moto.mock_sqs():
        yield boto3.resource("sqs")


@pytest.fixture
def queue(sqs):
    yield sqs.create_queue(QueueName="test-queue")


# ------------------------------------- DynamoDB ------------------------------------- #
@pytest.fixture
def dynamodb(aws_credentials):
    with moto.mock_dynamodb2():
        yield boto3.resource("dynamodb")


@pytest.fixture
def blunders_table_name():
    table_name = "test-blunders-table"
    original = os.getenv("BLUNDERS_TABLE_NAME")
    os.environ["BLUNDERS_TABLE_NAME"] = table_name
    yield table_name
    if original is None:
        os.environ.pop("BLUNDERS_TABLE_NAME")
    else:
        os.environ["BLUNDERS_TABLE_NAME"] = original


@pytest.fixture
def empty_blunders_table(dynamodb, blunders_table_name):
    table = dynamodb.create_table(
        TableName=blunders_table_name,
        AttributeDefinitions=[
            {"AttributeName": "job_name", "AttributeType": "S"},
            {"AttributeName": "created_at", "AttributeType": "S"},
        ],
        KeySchema=[
            {"AttributeName": "job_name", "KeyType": "HASH"},
            {"AttributeName": "created_at", "KeyType": "RANGE"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1,
        },
    )

    yield table


@pytest.fixture
def blunders_table(empty_blunders_table):
    table = empty_blunders_table
    with open(
        pathlib.Path(__file__)
        .parent.absolute()
        .joinpath("fixtures", "api", "blunders_table.json")
    ) as f:
        data = json.load(f)

    for item in data:
        table.put_item(Item=item)


# --------------------------------------- Other -------------------------------------- #
@pytest.fixture
def websocket_api_url():
    api_url = "https://test-api-url.com/"
    original = os.getenv("WEBSOCKET_API_URL")
    os.environ["WEBSOCKET_API_URL"] = api_url
    yield api_url
    if original is None:
        os.environ.pop("WEBSOCKET_API_URL")
    else:
        os.environ["WEBSOCKET_API_URL"] = original


# ------------------------------------------------------------------------------------ #
#                                      AWS events                                      #
# ------------------------------------------------------------------------------------ #
def aws_events(name: str):
    name = name if name.endswith(".json") else name + ".json"
    with open(
        pathlib.Path(__file__).parent.absolute().joinpath("fixtures", "api", name)
    ) as f:
        return json.load(f)


@pytest.fixture
def get_games_chessdotcom_invalid_username_event():
    event = aws_events("get_games_chessdotcom_events")[0]
    bad_username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=40))
    original_username = event["pathParameters"]["username"]
    return json.loads(json.dumps(event).replace(original_username, bad_username))


@pytest.fixture
def get_games_chessdotcom_invalid_query_params_event():
    event = aws_events("get_games_chessdotcom_events")[0]
    event["queryStringParameters"] = {"limit": -1}
    return event


# ------------------------------------------------------------------------------------ #
#                                     AWS contexts                                     #
# ------------------------------------------------------------------------------------ #
@pytest.fixture
def null_context():
    return None
