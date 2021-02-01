import asyncio
import io
import logging
import os
from copy import deepcopy
from math import exp
from typing import List, Optional

import chess
import chess.engine
import chess.pgn

from .models import Blunder, BlunderThreshold, Game

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
DEFAULT_ENGINE = os.environ["CHESS_BLUNDERS_ENGINE"]
MATE_SCORE = 100_000


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
    n_engines: int = 1,
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
        n_engines: number of concurrent engines to use to analyze the position.

    Returns:
        list of blunders data models.
    """
    engine_path = engine_path or DEFAULT_ENGINE
    scores_by_ply = {}

    async def score(
        position: str, side: chess.Color, engine: chess.engine.Protocol
    ) -> float:
        """
        Return the score of a given FEN position.
        """
        engine._ucinewgame()  # for deterministic results
        board = chess.Board(position)
        result = await engine.analyse(
            board,
            chess.engine.Limit(nodes=nodes),
            info=chess.engine.INFO_SCORE,
        )
        return getattr(
            result["score"], {chess.WHITE: "white", chess.BLACK: "black"}[side]
        )().score(mate_score=MATE_SCORE)

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

        solution_score = solution["score"].white().score(mate_score=MATE_SCORE)
        refutation_score = refutation["score"].white().score(mate_score=MATE_SCORE)
        solution_probability_score = _logistic(solution_score, scale=logistic_scale)
        refutation_probability_score = _logistic(refutation_score, scale=logistic_scale)
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
                "cp_loss": sign * (refutation_score - solution_score),
                "probability_loss": round(
                    sign * (refutation_probability_score - solution_probability_score),
                    2,
                ),
                "pgn": str(node),
            }
        )

        return blunder

    async def scorer(queue: asyncio.Queue) -> None:
        """
        Worker that scores positions from a queue.
        """
        try:
            _, engine = await chess.engine.popen_uci(engine_path)
            await engine.configure(engine_options)
            while True:
                ply, position = await queue.get()
                scores_by_ply[ply] = await score(position, side, engine)
                queue.task_done()
        finally:
            await engine.quit()

    # create the fen of each position and push it in the work queue
    positions: asyncio.Queue = asyncio.Queue()
    board = chess.Board()
    root = chess.pgn.read_game(io.StringIO(game.pgn))
    positions.put_nowait((board.ply(), chess.STARTING_FEN))
    for move in root.mainline_moves():
        board.push(move)
        positions.put_nowait((board.ply(), board.fen()))
    n_plies = board.ply()

    # calculate the score at each position
    workers = [asyncio.create_task(scorer(positions)) for _ in range(n_engines)]
    await positions.join()
    [worker.cancel() for worker in workers]
    await asyncio.gather(*workers, return_exceptions=True)
    scores = [scores_by_ply[ply] for ply in range(n_plies)]
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
