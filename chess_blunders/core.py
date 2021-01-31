import asyncio
import io
import os
from math import exp
from typing import Optional

import chess
import chess.engine
import chess.pgn

from .models import BlunderThreshold, Game, Line, SideEnum

DEFAULT_ENGINE = os.environ["CHESS_BLUNDERS_ENGINE"]


async def blunders(
    game: Game,
    *,
    threshold: BlunderThreshold = BlunderThreshold(),
    side: SideEnum = SideEnum(),
    nodes: int = 1_000_000,
    engine_path: Optional[str] = None,
) -> Line:
    """
    Checks if the latest move in a game was a blunder.
    """
    engine_path = engine_path or DEFAULT_ENGINE

    # create the fen of each position
    board = chess.Board()
    game_tree = chess.pgn.read_game(io.StringIO(game.pgn))
    positions = [chess.STARTING_FEN]
    for move in game_tree.mainline_moves():
        board.push(move)
        positions.append(board.fen())

    # calculate the score at each position
    async def score(position):
        try:
            _, engine = await chess.engine.popen_uci(engine_path)
            board = chess.Board(position)
            result = await engine.analyse(
                board,
                chess.engine.Limit(nodes=nodes),
                info=chess.engine.INFO_SCORE,
            )
        finally:
            await engine.quit()
        return getattr(result["score"], side)().cp

    scores = await asyncio.gather(
        *(asyncio.create_task(score(position)) for position in positions)
    )

    # look for blunders by the player we're interested in
    winning_chances = [
        1 / (1 + exp(-0.004 * score)) for score in scores
    ]  # https://lichess.org/blog/WFvLpiQAACMA8e9D/learn-from-your-mistakes

    return scores
