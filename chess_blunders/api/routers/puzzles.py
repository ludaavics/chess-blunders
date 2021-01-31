import asyncio
import logging
from typing import List, Union

from fastapi import APIRouter, status

from ... import core
from ...models import Blunder, Game

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.post(
    "/blunders", response_model=List[Blunder], status_code=status.HTTP_201_CREATED
)
async def create_blunder_puzzles(games: Union[Game, List[Game]]) -> List[Blunder]:
    """
    Create puzzles from blunders in a list of game.
    """
    if isinstance(games, Game):
        games = [games]
    blunders_by_game = await asyncio.gather(
        *(asyncio.create_task(core.blunders(game)) for game in games)
    )
    blunders = [
        blunder for game_blunders in blunders_by_game for blunder in game_blunders
    ]
    return blunders
