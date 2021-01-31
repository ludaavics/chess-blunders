import asyncio
import io
import os
from copy import deepcopy
from math import exp
from typing import List, Optional

import chess
import chess.engine
import chess.pgn

from .models import Blunder, BlunderThreshold, Game

DEFAULT_ENGINE = os.environ["CHESS_BLUNDERS_ENGINE"]


def _logistic(score, *, scale=0.004):
    """
    Convert a centi-pawn score to a win probability.
    """
    # choice of default scale is from
    # https://lichess.org/blog/WFvLpiQAACMA8e9D/learn-from-your-mistakes
    return 1 / (1 + exp(-scale * score))


async def blunders(
    game: Game,
    *,
    threshold: BlunderThreshold = BlunderThreshold(),
    side: chess.Color = chess.WHITE,
    nodes: int = 1_000_000,
    max_variation_plies: Optional[int] = None,
    logistic_scale: float = 0.004,
    engine_path: Optional[str] = None,
    engine_options: Optional[dict] = {"Hash": 256, "Threads": 1},
) -> List[Blunder]:
    """
    Return all the blunders in a game.

    Args:
        game: chess game data model.
        threshold: threshold if probability-of-winning loss to be considered a blunder.
        side: the side we monitor for blunders. chess.WHITE (a.k.a ``True`)
            or chess.Black (a.k.a ``False``).
        nodes: number of nodes to explore.
        max_variation_plies: maximum number of plies in the refutations and solutions.
        logistic_scale: scale (a.k.a growth rate) of the logistic curve used to convert
            centi-pawn scores to probabilities-of-winning.
        engine_path: path to the UCI or XBoard engine.
        engine_options: options passed to the UCI or XBoard engine.

    Returns:
        list of blunders data models.
    """

    async def score(position: str, side: chess.Color) -> float:
        """
        Return the score of a given FEN position.
        """
        try:
            _, engine = await chess.engine.popen_uci(engine_path)
            await engine.configure(engine_options)
            board = chess.Board(position)
            result = await engine.analyse(
                board,
                chess.engine.Limit(nodes=nodes),
                info=chess.engine.INFO_SCORE,
            )
        finally:
            await engine.quit()
        return getattr(
            result["score"], {chess.WHITE: "white", chess.BLACK: "black"}[side]
        )().cp

    async def add_lines(node: chess.pgn.GameNode) -> Blunder:
        """
        Add solution and refutation lines to a game node.
        """
        node = deepcopy(node)
        try:
            _, engine = await chess.engine.popen_uci(engine_path)
            await engine.configure(engine_options)
            _solution = asyncio.create_task(
                engine.analyse(
                    node.board(),
                    chess.engine.Limit(nodes=nodes),
                    info=(chess.engine.INFO_SCORE | chess.engine.INFO_PV),
                )
            )
            _, engine = await chess.engine.popen_uci(engine_path)
            await engine.configure(engine_options)
            _refutation = asyncio.create_task(
                engine.analyse(
                    node.next().board(),
                    chess.engine.Limit(nodes=nodes),
                    info=(chess.engine.INFO_SCORE | chess.engine.INFO_PV),
                )
            )
            solution, refutation = await asyncio.gather(_solution, _refutation)
        finally:
            await engine.quit()

        solution_score = solution["score"].white()
        refutation_score = refutation["score"].white()
        node.add_line(
            solution["pv"][:max_variation_plies],
            starting_comment=f"Solution ({solution_score})",
        )
        node.add_line(
            [node.next().move] + refutation["pv"][:max_variation_plies],
            starting_comment=f"Refutation ({refutation_score})",
        )

        sign = 1 if node.turn() == chess.WHITE else -1
        blunder = Blunder(
            **{
                "starting_fen": node.board().fen(),
                "cp_loss": sign * (refutation_score.cp - solution_score.cp),
                "probability_loss": sign
                * (
                    _logistic(refutation_score.cp, scale=logistic_scale)
                    - _logistic(solution_score.cp, scale=logistic_scale)
                ),
                "pgn": str(node),
            }
        )

        return blunder

    engine_path = engine_path or DEFAULT_ENGINE

    # create the fen of each position
    board = chess.Board()
    root = chess.pgn.read_game(io.StringIO(game.pgn))
    positions = [chess.STARTING_FEN]
    for move in root.mainline_moves():
        board.push(move)
        positions.append(board.fen())

    # calculate the score at each position
    scores = await asyncio.gather(
        *(asyncio.create_task(score(position, side)) for position in positions)
    )
    winning_chances = [_logistic(cp, scale=logistic_scale) for cp in scores]

    # look for blunders by the player we're interested in
    blunder_nodes = []
    for ply in range(len(winning_chances)):
        if ply == 0:
            continue
        white_is_playing = ply % 2
        side_is_white = side == chess.WHITE
        is_blunder = (
            winning_chances[ply] - winning_chances[ply - 1]
        ) <= -threshold.threshold
        if (white_is_playing == side_is_white) and is_blunder:
            node = root
            for _ in range(ply - 1):
                node = node.next()
            assert node.turn() == side
            blunder_nodes.append(node)

    # add solution and refutation lines
    blunders = await asyncio.gather(
        *(asyncio.create_task(add_lines(node)) for node in blunder_nodes)
    )

    return blunders
