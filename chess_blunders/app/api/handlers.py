import asyncio
import inspect
import json
import logging
import os
import time
from typing import List, Optional

import boto3
import wrapt
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
from chess_blunders.models import Color, Game

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

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
            true_handler = getattr(handler, "raw_function", handler)
            if inspect.iscoroutinefunction(true_handler):
                return await handler(**handler_kwargs)
            return handler(**handler_kwargs)
        except ValidationError as exc:
            return make_response(400, exc.errors())
        except HTTPError as exc:
            return requests_http_error_handler(exc)

    return asyncio.run(handle())


# ------------------------------------------------------------------------------------ #
#                                        Workers                                       #
# ------------------------------------------------------------------------------------ #
# async def blunders_worker(
#     games: List[Game],
#     colors: Optional[List[Color]] = None,
#     threshold: confloat(gt=0.0, lt=1.0) = 0.25,  # type: ignore
#     nodes: PositiveInt = 500_000,
#     max_variation_plies: Optional[PositiveInt] = None,
#     logistic_scale: PositiveFloat = 0.004,
# ):
#     pass


def blunders_worker(event, context):
    print(event)


# ------------------------------------------------------------------------------------ #
#                                       Handlers                                       #
# ------------------------------------------------------------------------------------ #
@http_handler
@validate_arguments
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
@validate_arguments
async def post_blunders(
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
    sns = boto3.client("sns")
    jobs_topic_arn = os.getenv("JOBS_TOPIC_ARN")
    job = {
        "games": [game.dict() for game in games],
        "colors": colors,
        "threshold": threshold,
        "nodes": nodes,
        "max_variation_plies": max_variation_plies,
        "logistic_scale": logistic_scale,
    }
    pub = sns.publish(TopicArn=jobs_topic_arn, Message=json.dumps(job))
    logger.debug(f"Scrape job published: {str(pub)}")

    # send response
    response = {"sns_response": pub}
    return make_response(202, response)

    blunders = await core.blunders.raw_function(
        games,
        colors=colors,
        threshold=threshold,
        nodes=nodes,
        max_variation_plies=max_variation_plies,
        logistic_scale=logistic_scale,
        engine_options={"Hash": 256, "Threads": 1},
        n_engines=-2,
    )

    blunders_dict = [blunder.dict() for blunder in blunders]
    return make_response(200, blunders_dict)
