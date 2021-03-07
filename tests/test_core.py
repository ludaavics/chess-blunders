import asyncio

import pytest

import chess_blunders


@pytest.mark.parametrize("games_loc,use_queue", [(0, False), (slice(1, 3), True)])
@pytest.mark.asyncio
async def test_known_blunders(games, games_loc, use_queue, snapshot):
    queue = asyncio.Queue() if use_queue else None
    blunders = await chess_blunders.blunders(
        games[games_loc],
        nodes=100_000,
        max_variation_plies=1,
        n_engines=-2,
        results=queue,
    )
    snapshot.assert_match([blunder.dict() for blunder in blunders])


@pytest.mark.asyncio
async def test_blunders_validation(games, snapshot):

    with pytest.raises(ValueError):
        await chess_blunders.blunders(games, colors=["black"] * (len(games) - 1))


@pytest.mark.asyncio
async def test_queue_runtime_error(games, caplog):
    queue = asyncio.Queue(1)
    tmp = chess_blunders.core.MATE_SCORE
    chess_blunders.core.MATE_SCORE = "foo"
    await chess_blunders.blunders(
        games[2],
        nodes=100_000,
        max_variation_plies=None,
        n_engines=-2,
        results=queue,
    )
    chess_blunders.core = tmp

    for record in caplog.records:
        try:
            assert "bad operand type" in record.message
            return
        except AssertionError:
            pass
    assert False
