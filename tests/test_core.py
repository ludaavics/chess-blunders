import pytest

import chess_blunders
from chess_blunders.models import Game


@pytest.mark.asyncio
async def test_known_blunders(games, snapshot):
    blunders = await chess_blunders.blunders(Game(**games[0]))
