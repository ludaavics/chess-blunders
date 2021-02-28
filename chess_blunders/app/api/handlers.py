import asyncio
import inspect
import json
import logging
import os
import random
import time
from datetime import datetime
from typing import Any, List, Optional

import boto3
import httpx
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

from chess_blunders import __version__, core
from chess_blunders.app.api.exc import requests_http_error_handler
from chess_blunders.models import Blunder, Color, Game

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CHESSDOTCOM_API_HOST = "https://api.chess.com/"
USER_AGENT = (
    f"chess-blunders/{__version__} (https://github.com/ludaavics/chess-blunders)"
)


# ------------------------------------------------------------------------------------ #
#                                        Helpers                                       #
# ------------------------------------------------------------------------------------ #
def make_response(status_code, body):
    return {"statusCode": status_code, "body": json.dumps(body, indent=2)}


@wrapt.decorator
def ws_handler(handler, instance, args, kwargs):
    assert len(args) == 2
    assert not kwargs
    event, context = args

    handler_kwargs = {"connection_id": event["requestContext"]["connectionId"]}
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
            return make_response(200, "")
        except HTTPError as exc:
            logger.exception(exc)
            return make_response(200, "")

    return asyncio.run(handle())


@wrapt.decorator
def sns_handler(handler, instance, args, kwargs):
    assert len(args) == 2
    assert not kwargs
    event, context = args
    assert len(event["Records"]) == 1

    enveloppe = event["Records"][0]["Sns"]
    handler_kwargs = json.loads(enveloppe["Message"])
    message_attributes = enveloppe.get("MessageAttributes", {})
    handler_kwargs.update(
        {k: message_attributes[k]["Value"] for k in message_attributes}
    )

    async def handle():
        _handler = validate_arguments(handler)
        if inspect.iscoroutinefunction(handler):
            return await _handler(**handler_kwargs)
        return _handler(**handler_kwargs)

    return asyncio.run(handle())


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
    connection_id: Optional[str] = None,
):
    sns = boto3.resource("sns")
    blunders_topic = sns.Topic(os.environ["BLUNDERS_TOPIC_ARN"])

    async def publish_blunder(queue: asyncio.Queue):
        while True:
            blunder = await queue.get()
            message = {"job_name": job_name, "blunder": blunder.dict()}
            attributes = {
                "connection_id": {
                    "DataType": "String",
                    "StringValue": str(connection_id),
                }
            }
            try:
                blunders_topic.publish(
                    Message=json.dumps(message), MessageAttributes=attributes
                )
            except Exception as e:
                logger.exception(e)
            finally:
                queue.task_done()

    results: asyncio.Queue = asyncio.Queue()
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


@sns_handler
def blunders_to_db(job_name: str, blunder: Blunder, **kwargs: Any):
    dynamodb = boto3.resource("dynamodb")
    blunders_table = dynamodb.Table(os.getenv("BLUNDERS_TABLE_NAME"))

    now = datetime.utcnow().isoformat()
    item = blunder.dict()
    item.update({"job_name": job_name, "created_at": now})

    # dynamo db refuses python floats
    # https://github.com/boto/boto3/pull/2699
    item["cp_loss"] = str(round(item["cp_loss"], 0))
    item["probability_loss"] = str(round(item["probability_loss"], 4))

    try:
        blunders_table.put_item(Item=item)
    except Exception as e:
        logger.exception(e)

    return item


@sns_handler
def blunders_to_ws(connection_id: str, blunder: Blunder, **kwargs: Any):
    api_endpoint = os.environ["WEBSOCKET_API_URL"]
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=api_endpoint)
    gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(blunder.dict(), indent=2).encode("utf-8"),
    )


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
async def connect(connection_id: str):
    return make_response(200, "")


@ws_handler
async def disconnect(connection_id: str):
    return make_response(200, "")


@ws_handler
def default(connection_id: str, **kwargs: Any):
    api_endpoint = os.environ["WEBSOCKET_API_URL"]
    msg = {"error": "Action not found.", "body": kwargs}
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=api_endpoint)
    gatewayapi.post_to_connection(
        ConnectionId=connection_id, Data=json.dumps(msg, indent=2).encode("utf-8")
    )
    return make_response(200, "")


@ws_handler
async def request_blunders(
    connection_id: str,
    username: str,
    source: str,
    *,
    threshold: confloat(gt=0.0, lt=1.0) = 0.25,  # type: ignore
    nodes: PositiveInt = 500_000,
    max_variation_plies: Optional[PositiveInt] = None,
    logistic_scale: PositiveFloat = 0.004,
    n_games: int = 5,
):
    jobs_topic_arn = os.environ["JOBS_TOPIC_ARN"]
    if source == "chess.com":
        return await request_blunders_chessdotcom(
            connection_id,
            username,
            threshold=threshold,
            nodes=nodes,
            max_variation_plies=max_variation_plies,
            logistic_scale=logistic_scale,
            jobs_topic_arn=jobs_topic_arn,
            n_games=n_games,
        )
    else:
        # send an error message and kill the connection
        pass


async def request_blunders_chessdotcom(
    connection_id: str,
    username: str,
    *,
    threshold: confloat(gt=0.0, lt=1.0),  # type: ignore
    nodes: PositiveInt,
    max_variation_plies: Optional[PositiveInt],
    logistic_scale: PositiveFloat,
    n_games: int,
    jobs_topic_arn: str,
):
    """
    Request blunders from randomly chosen games of a given chess.com user.
    """
    headers = {"user-agent": USER_AGENT}
    async with httpx.AsyncClient(
        base_url=CHESSDOTCOM_API_HOST, headers=headers
    ) as client:
        all_months = await client.get(f"pub/player/{username}/games/archives")
        all_months.raise_for_status()
        selected_months = random.choices(all_months.json()["archives"], k=n_games)

        requests = [asyncio.create_task(client.get(month)) for month in selected_months]
        for request in asyncio.as_completed(requests):
            games_in_month = await request
            sleep = 1
            while games_in_month.status_code == 429:
                msg = (
                    f"Sleeping for {sleep}s while "
                    f"getting chess.com games for {username}."
                )
                logger.debug(msg)
                await asyncio.sleep(sleep)
                sleep *= 2
                games_in_month = await client.get(games_in_month.url)

            games_in_month.raise_for_status()
            game = random.choice(games_in_month.json()["games"])
            game["white"]["name"] = game["white"].pop("username")
            game["white"]["url"] = game["white"].pop("@id")
            game["black"]["name"] = game["black"].pop("username")
            game["black"]["url"] = game["black"].pop("@id")
            game["eco_url"] = game.pop("eco", None)
            game["tournament_url"] = game.pop("tournament", None)
            game["match_url"] = game.pop("match", None)
            color = (
                "white"
                if game["white"]["name"].lower() == username.lower()
                else "black"
            )
            assert game[color]["name"].lower() == username.lower()

            # publish the job
            sns = boto3.resource("sns")
            jobs_topic = sns.Topic(jobs_topic_arn)
            job = {
                "job_name": connection_id,
                "connection_id": connection_id,
                "games": [Game(**game).dict()],
                "colors": [color],
                "threshold": threshold,
                "nodes": nodes,
                "max_variation_plies": max_variation_plies,
                "logistic_scale": logistic_scale,
            }
            jobs_topic.publish(Message=json.dumps(job))

    return make_response(200, "")
