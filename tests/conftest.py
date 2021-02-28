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

    return


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


# ------------------------------------------------------------------------------------ #
#                                      AWS events                                      #
# ------------------------------------------------------------------------------------ #
def event(name: str):
    name = name if name.endswith(".json") else name + ".json"
    with open(
        pathlib.Path(__file__).parent.absolute().joinpath("fixtures", "api", name)
    ) as f:
        return json.load(f)


@pytest.fixture
def request_blunders_events():
    return event("request_blunders_events")


@pytest.fixture
def get_games_chessdotcom_event():
    return event("get_games_chessdotcom_event")


@pytest.fixture
def get_games_chessdotcom_invalid_username_event(get_games_chessdotcom_event):
    event = get_games_chessdotcom_event
    bad_username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=40))
    original_username = event["pathParameters"]["username"]
    return json.loads(
        json.dumps(get_games_chessdotcom_event).replace(original_username, bad_username)
    )


@pytest.fixture
def get_games_chessdotcom_invalid_query_params_event(get_games_chessdotcom_event):
    event = get_games_chessdotcom_event
    event["queryStringParameters"] = {"limit": -1}
    return event


@pytest.fixture
def post_blunders_events():
    return event("post_blunders_events")


@pytest.fixture
def get_blunders_events():
    return event("get_blunders_events")


@pytest.fixture
def blunders_job_events():
    return event("blunders_job_events")


def blunders_events():
    return event("blunders_events")


# ------------------------------------------------------------------------------------ #
#                                     AWS contexts                                     #
# ------------------------------------------------------------------------------------ #
@pytest.fixture
def null_context():
    return None
