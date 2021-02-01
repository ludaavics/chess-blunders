import pytest

import chess_blunders
from chess_blunders.models import Game


@pytest.mark.asyncio
async def test_known_blunders(games, snapshot):
    blunders = await chess_blunders.blunders(
        Game(**games[0]), max_variation_plies=1, n_engines=10
    )
    snapshot.assert_match([blunder.dict() for blunder in blunders])
