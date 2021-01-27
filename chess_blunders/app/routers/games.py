import logging
import time
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from requests.compat import urljoin  # type: ignore
from requests_futures.sessions import FuturesSession

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
router = APIRouter(prefix="/games", tags=["games"])
CHESSDOTCOM_API_HOST = "https://api.chess.com/"


class Player(BaseModel):
    username: str
    url: str
    rating: int
    result: str


class Game(BaseModel):
    url: Optional[str]
    white: Player
    black: Player
    pgn: str
    fen: str
    start_time: Optional[int]
    end_time: int
    time_control: str
    rules: str
    eco_url: Optional[str]
    tournament_url: Optional[str]
    match_url: Optional[str]


@router.get("/chessdotcom/{username}", response_model=List[Game])
def get_games_chessdotcom(username: str, limit: int = 10):
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
                game["white"]["url"] = game["white"].pop("@id")
                game["black"]["url"] = game["black"].pop("@id")
                game["eco_url"] = game.pop("eco", None)
                game["tournament_url"] = game.pop("tournament", None)
                game["match_url"] = game.pop("match", None)
                games.append(game)
                if len(games) >= limit:
                    break

            if len(games) >= limit:
                break

    return games[:limit]
