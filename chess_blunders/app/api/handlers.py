import asyncio
import json
import logging
import time
from typing import List

import wrapt
from pydantic import PositiveInt, ValidationError, validate_arguments
from requests import HTTPError
from requests.compat import urljoin  # type: ignore
from requests_futures.sessions import FuturesSession

from chess_blunders.app.api.exc import requests_http_error_handler
from chess_blunders.models import Game

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

CHESSDOTCOM_API_HOST = "https://api.chess.com/"


# ------------------------------------------------------------------------------------ #
#                                        Helpers                                       #
# ------------------------------------------------------------------------------------ #
def jsonify(status_code, body):
    return {"statusCode": status_code, "body": json.dumps(body, indent=2)}


@wrapt.decorator
def async_handler(handler, instance, args, kwargs):
    assert len(args) == 2
    assert not kwargs
    event, context = args
    handler_kwargs = {}
    handler_kwargs.update(event["pathParameters"])

    async def handle():
        try:
            return handler(**handler_kwargs)
        except ValidationError as exc:
            return jsonify(400, exc.errors())
        except HTTPError as exc:
            return requests_http_error_handler(exc)

    return asyncio.run(handle())


# ------------------------------------------------------------------------------------ #
#                                       Handlers                                       #
# ------------------------------------------------------------------------------------ #
@async_handler
@validate_arguments
def get_games_chessdotcom(username: str, limit: PositiveInt = 10) -> List[Game]:
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

    return jsonify(200, games[:limit])


@async_handler
async def blunders(event, context):
    """
    Create puzzles from blunders in a list of games.
    """
    data = json.loads(event.get("body", "{}"))
    return jsonify(200, data)
