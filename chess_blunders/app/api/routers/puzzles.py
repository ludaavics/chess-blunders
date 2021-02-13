import logging
from typing import List

from fastapi import APIRouter, Depends, status

from chess_blunders import core
from chess_blunders.app.api.dependencies import BlunderParameters  # TO FIX
from chess_blunders.models import Blunder, Color, Game

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.post(
    "/blunders", response_model=List[Blunder], status_code=status.HTTP_201_CREATED
)
async def create_blunder_puzzles(
    games: List[Game],
    blunder_parameters: BlunderParameters = Depends(),
) -> List[Blunder]:
    """
    Create puzzles from blunders in a list of games.
    """
    if blunder_parameters.colors is None:
        blunder_parameters.colors = [Color.white for _ in range(len(games))]
    return await core.blunders(
        games,
        **vars(blunder_parameters),
        engine_options={"Hash": 256, "Threads": 1},
        n_engines=10
    )
