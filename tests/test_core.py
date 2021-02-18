import pytest

import chess_blunders


@pytest.mark.parametrize("games_loc", [0, slice(1, 3)])
@pytest.mark.asyncio
async def test_known_blunders(games, games_loc, snapshot):
    blunders = await chess_blunders.blunders(
        games[games_loc], max_variation_plies=1, n_engines=-2
    )
    snapshot.assert_match([blunder.dict() for blunder in blunders])


@pytest.mark.asyncio
async def test_blunders_validation(games, snapshot):

    with pytest.raises(ValueError):
        await chess_blunders.blunders(games, colors=["black"] * (len(games) - 1))
