import asyncio
import inspect
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, List, Optional

import aioboto3
import boto3
import wrapt
from boto3.dynamodb.conditions import Key
from haikunator import Haikunator
from pydantic import (
    PositiveFloat,
    PositiveInt,
    ValidationError,
    confloat,
    validate_arguments,
)
from requests import HTTPError
from requests.compat import urljoin  # type: ignore
from requests_futures.sessions import FuturesSession

from chess_blunders import core
from chess_blunders.app.api.exc import requests_http_error_handler
from chess_blunders.models import Blunder, Color, Game

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CHESSDOTCOM_API_HOST = "https://api.chess.com/"


# ------------------------------------------------------------------------------------ #
#                                        Helpers                                       #
# ------------------------------------------------------------------------------------ #
def make_response(status_code, body):
    return {"statusCode": status_code, "body": json.dumps(body, indent=2)}


@wrapt.decorator
def http_handler(handler, instance, args, kwargs):
    assert len(args) == 2
    assert not kwargs
    event, context = args
    handler_kwargs = {}
    handler_kwargs.update(event.get("pathParameters", {}))
    handler_kwargs.update(event.get("queryStringParameters", {}))
    handler_kwargs.update(json.loads(event.get("body", "{}")))

    async def handle():
        try:
            _handler = validate_arguments(handler)
            if inspect.iscoroutinefunction(handler):
                return await _handler(**handler_kwargs)
            return _handler(**handler_kwargs)
        except ValidationError as exc:
            logger.exception(exc.errors())
            return make_response(400, exc.errors())
        except HTTPError as exc:
            logger.exception(exc)
            return requests_http_error_handler(exc)

    return asyncio.run(handle())


@wrapt.decorator
def sns_handler(handler, instance, args, kwargs):
    assert len(args) == 2
    assert not kwargs
    event, context = args
    assert len(event["Records"]) == 1

    message = json.loads(event["Records"][0]["Sns"]["Message"])

    async def handle():
        _handler = validate_arguments(handler)
        if inspect.iscoroutinefunction(handler):
            return await _handler(**message)
        return _handler(**message)

    return asyncio.run(handle())


@wrapt.decorator
def ws_handler(handler, instance, args, kwargs):
    assert len(args) == 2
    assert not kwargs
    event, context = args

    connection_id = event["requestContext"]["connectionId"]
    domain_name = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    api_endpoint = f"https://{domain_name}/{stage}"
    handler_kwargs = {"connection_id": connection_id, "api_endpoint": api_endpoint}
    body = event.get("body", "{}")
    try:
        body = json.loads(body)
    except ValueError:
        body = {"body": body}
    body.pop("action", None)
    handler_kwargs.update(body)

    async def handle():
        try:
            _handler = validate_arguments(handler)
            if inspect.iscoroutinefunction(handler):
                return await _handler(**handler_kwargs)
            return _handler(**handler_kwargs)
        except ValidationError as exc:
            logger.exception(exc.errors())
            return make_response(400, exc.errors())
        except HTTPError as exc:
            logger.exception(exc)
            return requests_http_error_handler(exc)

    return asyncio.run(handle())


# ------------------------------------------------------------------------------------ #
#                                        Workers                                       #
# ------------------------------------------------------------------------------------ #
@sns_handler
async def blunders_worker(
    job_name: str,
    games: List[Game],
    colors: Optional[List[Color]] = None,
    threshold: confloat(gt=0.0, lt=1.0) = 0.25,  # type: ignore
    nodes: PositiveInt = 500_000,
    max_variation_plies: Optional[PositiveInt] = None,
    logistic_scale: PositiveFloat = 0.004,
):
    results: asyncio.Queue = asyncio.Queue()

    async def publish_blunder(queue: asyncio.Queue):
        async with aioboto3.resource("dynamodb") as dynamodb:
            blunders_table = await dynamodb.Table(os.getenv("BLUNDERS_TABLE_NAME"))
            while True:
                blunder = await queue.get()

                now = datetime.utcnow().isoformat()
                item = blunder.dict()
                item.update({"job_name": job_name, "created_at": now})

                # dynamo db refuses python floats
                # https://github.com/boto/boto3/pull/2699
                item["cp_loss"] = str(round(item["cp_loss"], 0))
                item["probability_loss"] = str(round(item["probability_loss"], 4))

                try:
                    await blunders_table.put_item(Item=item)
                except Exception as e:
                    logger.exception(e)
                finally:
                    queue.task_done()

    producers = asyncio.create_task(
        core.blunders.raw_function(
            games,
            colors=colors,
            threshold=threshold,
            nodes=nodes,
            max_variation_plies=max_variation_plies,
            logistic_scale=logistic_scale,
            engine_options={"Hash": 256, "Threads": 1},
            n_engines=-1,
            results=results,
        )
    )
    consumers = asyncio.create_task(publish_blunder(results))
    blunders = await producers
    await results.join()
    consumers.cancel()

    return [blunder.dict() for blunder in blunders]


# ------------------------------------------------------------------------------------ #
#                                    HTTP Endpoints                                    #
# ------------------------------------------------------------------------------------ #
@http_handler
def get_games_chessdotcom(username: str, limit: PositiveInt = 10) -> dict:
    """
    Get all the games from a chess.com user.
    """
    session = FuturesSession()

    # get the list of monthly archives
    url = urljoin(CHESSDOTCOM_API_HOST, f"pub/player/{username}/games/archives")
    archives = session.get(url).result()
    archives.raise_for_status()

    # fetch all the games
    games = []
    with FuturesSession() as session:
        futures = [session.get(url) for url in reversed(archives.json()["archives"])]
        for future in futures:
            monthly_games = future.result()
            sleep = 1
            while monthly_games.status_code == 429:  # pragma: no cover
                msg = (
                    f"Sleeping for {sleep}s while "
                    f"getting chess.com games for {username}."
                )
                logger.debug(msg)
                time.sleep(2 * sleep)
                monthly_games = session.get(url).result()
            monthly_games.raise_for_status()
            for game in monthly_games.json()["games"]:
                game["white"]["name"] = game["white"].pop("username")
                game["white"]["url"] = game["white"].pop("@id")
                game["black"]["name"] = game["black"].pop("username")
                game["black"]["url"] = game["black"].pop("@id")
                game["eco_url"] = game.pop("eco", None)
                game["tournament_url"] = game.pop("tournament", None)
                game["match_url"] = game.pop("match", None)
                games.append(game)
                if len(games) >= limit:
                    break

            if len(games) >= limit:
                break

    [Game(**game) for game in games[:limit]]  # just to push through model validation
    return make_response(200, games[:limit])


@http_handler
def post_blunders(
    games: List[Game],
    colors: Optional[List[Color]] = None,
    threshold: confloat(gt=0.0, lt=1.0) = 0.25,  # type: ignore
    nodes: PositiveInt = 500_000,
    max_variation_plies: Optional[PositiveInt] = None,
    logistic_scale: PositiveFloat = 0.004,
) -> dict:
    """
    Create puzzles from blunders in a list of games.
    """
    if colors is None:
        colors = [Color.white for _ in range(len(games))]

    # publish the job
    job_name = Haikunator().haikunate()
    sns = boto3.resource("sns")
    jobs_topic = sns.Topic(os.getenv("JOBS_TOPIC_ARN"))
    job = {
        "job_name": job_name,
        "threshold": threshold,
        "nodes": nodes,
        "max_variation_plies": max_variation_plies,
        "logistic_scale": logistic_scale,
    }
    for game, color in zip(games, colors):
        job.update({"games": [game.dict()], "colors": [color]})
        jobs_topic.publish(Message=json.dumps(job))

    # send response
    response = {"blunders": f"/blunders/{job_name}"}
    return make_response(202, response)


@http_handler
def get_blunders(job_name: str) -> List[Blunder]:

    dynamodb = boto3.resource("dynamodb")
    blunders_table = dynamodb.Table(os.getenv("BLUNDERS_TABLE_NAME"))
    blunders = [
        Blunder(**blunder).dict()
        for blunder in blunders_table.query(
            KeyConditionExpression=Key("job_name").eq(job_name)
        )["Items"]
    ]

    return make_response(200, blunders)


# ------------------------------------------------------------------------------------ #
#                                  WebSocket Endpoints                                 #
#                                                                                      #
#                                        connect                                       #
#                                      disconnect                                      #
#                                        default                                       #
#                                   request_blunders                                   #
# ------------------------------------------------------------------------------------ #
@ws_handler
async def connect(connection_id: str, api_endpoint: str):
    return make_response(200, "")


@ws_handler
async def disconnect(connection_id: str, api_endpoint: str):
    return make_response(200, "")


@ws_handler
def default(connection_id: str, api_endpoint: str, **kwargs: Any):
    msg = {"error": "Action not found.", "body": kwargs}
    return make_response(404, msg)


@ws_handler
async def request_blunders(
    connection_id: str,
    api_endpoint: str,
    username: str,
    source: str,
    *,
    n_games: int = 5,
    n_blunders: int = 20,
):
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=api_endpoint)
    msg = f"Requesting blunders for {username} on {source} for {connection_id}."
    return gatewayapi.post_to_connection(
        ConnectionId=connection_id, Data=msg.encode("utf-8")
    )
